var BundleTracker = require('webpack-bundle-tracker');
const path = require('path');
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
      'webpack-dev-server/client?http://' + process.env.PUBLIC_PATH + ':3000',
      'webpack/hot/dev-server',
      './src/index'
    ];
    config.output = {
      path:  path.resolve(__dirname, 'build/static/'),
      publicPath: 'http://' + process.env.PUBLIC_PATH + ':3000/',
    };
    config.optimization.splitChunks.name = 'vendors';

    // config.resolve = {
    //   ...config.resolve,
    //   alias: { '@': path.resolve(__dirname, 'front_end/src') },
    // };

    return config;
  },
  devServer: function(configFunction) {
    return function(proxy, allowedHost) {
      const config = configFunction(proxy, allowedHost);
      config.headers = {
        'Access-Control-Allow-Origin': '*'
      };
      config.hot = true;
      config.public = process.env.PUBLIC_PATH + ":3000";

      return config;
    };
  },
  paths: function (paths, env) {
      console.log(path.resolve(__dirname, 'src'));
      paths.appIndexJs = path.resolve(__dirname, 'src/index.js');
      paths.appSrc = path.resolve(__dirname, 'src');
      return paths;
  },
};

// ' + paths.serverHostname + '