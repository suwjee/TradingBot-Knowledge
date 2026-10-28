import path from 'node:path';
import fs from 'node:fs';

function isWithin(base, target) {
  const relative = path.relative(base, target);
  return !path.isAbsolute(relative) && relative !== '..' && !relative.startsWith(`..${path.sep}`);
}

/** Resolve local state within its dedicated chart-owned directory. */
export function resolveLocalStatePaths(workspaceRoot, configuredRoot = process.env.TRADINGBOT_LOCAL_STATE_ROOT) {
  const workspace = path.resolve(workspaceRoot);
  const stateDirectory = path.join(workspace, 'apps', 'chart', 'state');
  const root = configuredRoot?.trim()
    ? path.resolve(workspace, configuredRoot.trim())
    : stateDirectory;
  const error = 'TRADINGBOT_LOCAL_STATE_ROOT must use the dedicated chart state directory inside this project.';
  if (!isWithin(stateDirectory, root)) throw new Error(error);
  if (fs.existsSync(workspace)) {
    let ancestor = root;
    while (!fs.existsSync(ancestor)) ancestor = path.dirname(ancestor);
    const physicalRoot = path.resolve(fs.realpathSync(ancestor), path.relative(ancestor, root));
    const physicalStateDirectory = path.join(fs.realpathSync(workspace), 'apps', 'chart', 'state');
    if (!isWithin(physicalStateDirectory, physicalRoot)) throw new Error(error);
  }
  return Object.freeze({
    root,
    raw: path.join(root, 'data', 'raw'),
    cache: path.join(root, 'cache'),
    secret: path.join(root, 'secret'),
    tmp: path.join(root, 'tmp'),
  });
}
