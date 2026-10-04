const listeners = new Set();

const state = {
  violence: "alguna",
  age: "todas",
  depto: "peru",
};

export function getState() {
  return { ...state };
}

export function setState(patch) {
  Object.assign(state, patch);
  for (const fn of listeners) fn(getState());
}

export function subscribe(fn) {
  listeners.add(fn);
  return () => listeners.delete(fn);
}
