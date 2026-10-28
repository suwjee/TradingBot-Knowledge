export function resolveCanonicalChartPoint({
  x,
  y,
  timeAtCoordinate,
  priceAtCoordinate,
  fallback,
}) {
  const time = timeAtCoordinate(x);
  const price = priceAtCoordinate(y);
  return time == null || price == null ? fallback : { x, y, time, price };
}
