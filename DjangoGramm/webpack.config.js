const path = require('path')
const HTMLWebpuckPlugin = require('html-webpack-plugin')
const {CleanWebpackPlugin} = require('clean-webpack-plugin')
const MiniCssExtractPlugin = require("mini-css-extract-plugin")
const CssMinimizerWebpackPlugin = require('css-minimizer-webpack-plugin')
const TerserWebpackPlugin = require("terser-webpack-plugin");


module.exports = {
    context: path.resolve(__dirname, "djangogramm"),
    mode: 'development',
    entry: {
        delete_post: "./static/src/delete_post.js",
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
        new CleanWebpackPlugin(),
        new MiniCssExtractPlugin(
            {
                filename: "[name].[contenthash].css"
            }
        )
    ],
    optimization: {
        splitChunks: {
            chunks: 'all'
        },
        minimize: true,
        minimizer: [
            new CssMinimizerWebpackPlugin(
                {
                    test: /\.foo\.css$/i,
                    parallel: true
                }
            ),
            new TerserWebpackPlugin()
        ]
    },
    module: {
        rules: [
            {
                test: /\.css$/,
                use: [MiniCssExtractPlugin.loader, 'css-loader']
            },
            {
                test: /\.(woff(2)?|ttf|eot|png|jpg|svg|gif)$/,
                use: ['file-loader']
            },
            {
                test: /\.s[ac]ss$/,
                use: [MiniCssExtractPlugin.loader, 'css-loader', 'sass-loader']
            },
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader",
                    options: {
                        presets: ['@babel/preset-env']
                    }
                }
            }
        ]
    }
}