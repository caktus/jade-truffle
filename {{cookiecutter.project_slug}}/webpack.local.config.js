const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const baseConfig = require('./webpack.base.config');
const { merge } = require('webpack-merge');

module.exports = merge(baseConfig, {
  mode: 'development',
  devtool: 'inline-source-map',
  output: {
    path: path.resolve('./{{ cookiecutter.project_slug}}/static/bundles/'),
    filename: '[name].js',
  },
  plugins: [
    new webpack.EvalSourceMapDevToolPlugin({
      exclude: /node_modules/
    }),
    new BundleTracker({
      filename: './webpack-stats.json',
    }),
  ],
  optimization: {
    moduleIds: "named",
  }
});
