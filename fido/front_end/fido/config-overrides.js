var BundleTracker = require('webpack-bundle-tracker');
var webpack = require('webpack')

module.exports = {
  webpack: (config, env) => {
    config.plugins = [
    new webpack.HotModuleReplacementPlugin(),
    new BundleTracker({
        path: __dirname,
        filename: './config/webpack-stats.json',
      }),
    ];
    config.entry = [
      'webpack-dev-server/client?http://localhost:3000',
      'webpack/hot/dev-server',
      '/fido/front_end/fido/src/index'
    ];
    config.output = {
      path: '/fido/front_end/fido/build/static/',
      publicPath: 'http://localhost:3000/',
    };
    config.optimization.splitChunks.name = 'vendors';

    return config;
  },
  devServer: function(configFunction) {
    return function(proxy, allowedHost) {
      const config = configFunction(proxy, allowedHost);
      config.headers = {
        'Access-Control-Allow-Origin': '*'
      };
      config.hot = true;
      config.public = "localhost:3000";

      return config;
    };
  }
};

// ' + paths.serverHostname + '