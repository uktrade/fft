var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  webpack: (config, env) => {

    config.plugins.push(
      new BundleTracker({
        path: __dirname,
        filename: './config/webpack-stats.json',
      }),
    );

    // ' + paths.serverHostname + '

    // config.entry = [
    //     require.resolve('webpack-dev-server/client') + '?http://localhost:3000',
    //     require.resolve('webpack/hot/dev-server'),
    //   // Finally, this is your app's code:
    //   //config.paths.appIndexJs,
    // ]

  config.entry = [
      'webpack-dev-server/client?http://localhost:3000',
      'webpack/hot/only-dev-server',
      '/fido/front_end/fido/src/index.js'
  ],

    config.output = {
      path: '/fido/front_end/fido/build/static/',
      //filename: "[name].[hash].js",
      publicPath: 'http://localhost:3000/',
        //public: "http://localhost:3000"
    };

    config.optimization.splitChunks.name = 'vendors';

    return config;
  },
  devServer: function(configFunction) {
    // Return the replacement function for create-react-app to use to generate the Webpack
    // Development Server config. "configFunction" is the function that would normally have
    // been used to generate the Webpack Development server config - you can use it to create
    // a starting configuration to then modify instead of having to create a config from scratch.
    return function(proxy, allowedHost) {
      // Create the default config by calling configFunction with the proxy/allowedHost parameters
      const config = configFunction(proxy, allowedHost);

        config.headers = {
          'Access-Control-Allow-Origin': '*'
        }
        config.hot = true,
        config.public = "localhost:3000"

      // Return your customised Webpack Development Server config.
      return config;
    };
  },
};