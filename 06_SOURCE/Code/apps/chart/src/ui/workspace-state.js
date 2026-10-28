const contracts = {
  chart: {
    headerGroups: ["chart-left", "drawing", "chart-actions"],
    footerGroups: ["runtime", "market", "clock"],
  },
  algorithm: {
    headerGroups: ["workspace"],
    footerGroups: ["runtime", "clock"],
  },
  faraz: {
    headerGroups: ["workspace"],
    footerGroups: ["runtime", "clock"],
  },
  "fullscreen-chart": {
    headerGroups: [],
    footerGroups: [],
  },
};

export const WORKSPACE_CONTRACTS = Object.freeze(
  Object.fromEntries(Object.entries(contracts).map(([name, contract]) => [
    name,
    Object.freeze({
      headerGroups: Object.freeze([...contract.headerGroups]),
      footerGroups: Object.freeze([...contract.footerGroups]),
    }),
  ])),
);

export function workspaceContract(name) {
  const contract = WORKSPACE_CONTRACTS[name];
  if (!contract) throw new RangeError(`Unknown workspace: ${name}`);
  return contract;
}

export function applyWorkspaceState(root, name) {
  const contract = workspaceContract(name);
  const visible = new Set([...contract.headerGroups, ...contract.footerGroups]);
  root.dataset.workspace = name;
  for (const element of root.querySelectorAll("[data-workspace-group]")) {
    const isVisible = visible.has(element.dataset.workspaceGroup);
    element.hidden = !isVisible;
    element.inert = !isVisible;
    element.setAttribute("aria-hidden", String(!isVisible));
  }
  return contract;
}

export function mountWorkspaceHeader(slot, header) {
  if (!slot || !header) throw new TypeError("A shared Header slot and feature Header are required");
  slot.replaceChildren(header);
  slot.hidden = false;
}

export function restoreWorkspaceHeader(home, header) {
  if (!home || !header) throw new TypeError("A feature Header home and Header are required");
  home.prepend(header);
}
