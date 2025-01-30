export default function FeatureFlags(namespace) {
  const cache = new Map();

  const featureFlagHandler = {
    get(target, prop, receiver) {
      const selector = `meta[name="${namespace}:${prop}"]`;

      const el = document.querySelector(selector);

      if (!el) {
        return false;
      }

      if (cache.has(prop)) {
        return cache.get(prop);
      }

      const value = el.content.toLowerCase() === "true";

      cache.set(prop, value);

      return value;
    },
  };

  const featureFlagProxy = new Proxy({}, featureFlagHandler);

  return featureFlagProxy;
}
