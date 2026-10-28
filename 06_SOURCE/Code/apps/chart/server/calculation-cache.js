import fs from 'node:fs';
import path from 'node:path';

function rawDigestPath(resultPath) {
  return `${resultPath}.raw-sha256`;
}

export function cachePathForRaw(basePath, rawSha256, changedRawPath) {
  try {
    if (!fs.existsSync(basePath)) return basePath;
    return fs.readFileSync(rawDigestPath(basePath), 'utf8') === rawSha256 ? basePath : changedRawPath;
  } catch (error) {
    if (error?.code === 'ENOENT') return basePath;
    throw error;
  }
}

export function readCalculationCache(resultPath, rawSha256) {
  try {
    if (fs.readFileSync(rawDigestPath(resultPath), 'utf8') !== rawSha256) return null;
    return fs.readFileSync(resultPath, 'utf8');
  } catch (error) {
    if (error?.code === 'ENOENT') return null;
    throw error;
  }
}

export function writeCalculationCache(resultPath, rawSha256, result) {
  fs.mkdirSync(path.dirname(resultPath), { recursive: true });
  try {
    fs.unlinkSync(rawDigestPath(resultPath));
  } catch (error) {
    if (error?.code !== 'ENOENT') throw error;
  }
  fs.writeFileSync(resultPath, result, 'utf8');
  fs.writeFileSync(rawDigestPath(resultPath), rawSha256, 'utf8');
}
