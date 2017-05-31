const HtmlWebpackPlugin = require('html-webpack-plugin');
const path = require('path');
module.exports = {
  entry: "./src/index.js",
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "bundle.js"
  },
  plugins: [new HtmlWebpackPlugin()],
  module: {
    loaders: [
      { test: /\.css$/, loader: "style!css" },
      { test: /\.js/, exclude: /node_modules/, loader: "babel-loader" },
    ]
  }
}
