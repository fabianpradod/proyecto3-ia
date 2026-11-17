/* Pre-flight export bookmarklet.
   Run it on a Canvas assignment page, or on a course page for the assignment list,
   while logged in. It only sends GET requests to the same Canvas site and saves one
   JSON file to Downloads. Block comments only: a line comment would break the
   bookmark if a browser joined its lines. */
void (async () => {
  const FORMAT = 'preflight-export/1';
  const match = location.pathname.match(/\/courses\/(\d+)(?:\/assignments\/(\d+))?/);
  if (!match) {
    alert('Pre-flight: open a Canvas course or assignment page first.');
    return;
  }
  const courseId = Number(match[1]);
  const assignmentId = match[2] ? Number(match[2]) : null;
  const options = {headers: {Accept: 'application/json'}, credentials: 'same-origin'};

  const readJson = async (response, path) => {
    if (!response.ok) throw new Error(path + ' returned ' + response.status);
    return JSON.parse((await response.text()).replace(/^while\(1\);/, ''));
  };
  const get = async (path) => readJson(await fetch('/api/v1' + path, options), path);
  const getAll = async (path) => {
    let url = '/api/v1' + path;
    let items = [];
    while (url) {
      const response = await fetch(url, options);
      items = items.concat(await readJson(response, path));
      const next = (response.headers.get('Link') || '').split(',').find((part) => part.includes('rel="next"'));
      url = next ? next.slice(next.indexOf('<') + 1, next.indexOf('>')) : null;
    }
    return items;
  };

  const collect = async () => {
    const base = {format: FORMAT, base_url: location.origin, course_id: courseId, exported_at: new Date().toISOString()};
    if (assignmentId === null) {
      const assignments = await getAll('/courses/' + courseId + '/assignments?include[]=submission&order_by=due_at&per_page=100');
      return {name: 'preflight_' + courseId + '_assignments.json', data: {...base, kind: 'course', assignments}};
    }
    const prefix = '/courses/' + courseId + '/assignments/' + assignmentId;
    const assignment = await get(prefix);
    const submission = await get(prefix + '/submissions/self?include[]=submission_comments');
    const ids = [...(assignment.description || '').matchAll(/\/files\/(\d+)/g)].map((found) => Number(found[1]));
    const files = [];
    for (const id of [...new Set(ids)]) {
      try {
        files.push(await get('/files/' + id));
      } catch (error) {
        files.push({id, error: error.message});
      }
    }
    return {name: 'preflight_' + courseId + '_' + assignmentId + '.json', data: {...base, kind: 'assignment', assignment, submission, files}};
  };

  try {
    const result = await collect();
    if (window.__preflightDryRun) {
      window.__preflightResult = result;
      return;
    }
    const blob = new Blob([JSON.stringify(result.data, null, 2)], {type: 'application/json'});
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = result.name;
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(link.href), 1000);
  } catch (error) {
    alert('Pre-flight export failed: ' + error.message);
  }
})();
