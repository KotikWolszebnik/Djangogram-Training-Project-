const path = require('path')
const HTMLWebpuckPlugin = require('html-webpack-plugin')
const {CleanWebpackPlugin} = require('clean-webpack-plugin')

module.exports = {
    context: path.resolve(__dirname, "djangogramm"),
    mode: 'development',
    entry: {
        like_button: "./static/src/like_button.js",
        subscribe_button: "./static/src/subscribe_button.js"
    },
    output: {
        filename: "[name].[contenthash].js",
        path: path.resolve(__dirname, 'djangogramm/static/bundle/')
    },
    plugins: [
        new HTMLWebpuckPlugin(
            {
                template: "./templates/base.html"
            }
        ),
        new CleanWebpackPlugin()
    ],
    module: {
        rules: [
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader']
            }
        ]
    }
}