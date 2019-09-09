var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  webpack: (config, env) => {

    config.plugins.push(
      new BundleTracker({
        path: __dirname,
        filename: './config/webpack-stats.json',
      }),
    );

    config.optimization.splitChunks.name = 'vendors';

    return config;
  },
};