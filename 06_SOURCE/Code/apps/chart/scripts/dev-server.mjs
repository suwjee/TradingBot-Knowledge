import {
  spawn,
} from 'node:child_process'

import {
  existsSync,
} from 'node:fs'

import {
  resolve,
} from 'node:path'

const args = process.argv.slice(2)

const vite =
  resolve(
    process.cwd(),
    'node_modules',
    'vite',
    'bin',
    'vite.js',
  )

if (
  !existsSync(vite)
) {
  console.error(
    '[vite-dev] Vite was not found:',
  )

  console.error(vite)
  process.exit(1)
}

const child =
  spawn(
    process.execPath,

    [
      vite,
      ...args,
    ],

    {
      cwd:
        process.cwd(),

      stdio:
        'inherit',

      env: process.env,
    },
  )

child.once(
  'error',
  error => {
    console.error(error)
    process.exit(1)
  },
)

child.once(
  'exit',
  (
    code,
    signal,
  ) => {
    if (signal) {
      process.exit(0)
    }

    process.exit(
      code ?? 0,
    )
  },
)
