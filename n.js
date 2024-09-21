function areIsomorphic(a, b) {
  let m = a.length,
    n = b.length;

  if (m != n) {
    return false;
  }

  if (a.charCodeAt(0) > b.charCodeAt(0)) {
    [a, b] = [b, a];
  }

  const diff = b.charCodeAt(0) - a.charCodeAt(0);

  for (let i = 1; i < m; ++i) {
    if ((a.charCodeAt(i) - 96 + diff) % 26 != b.charCodeAt(i) - 96) {
      return false;
    }
  }

  return true;
}

console.log(areIsomorphic("aitg", "dphc"));
