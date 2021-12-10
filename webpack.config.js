const webpack = require('webpack');
const path = require('path');

module.exports = {
    bail: true,
    context: __dirname,
    entry: ['./{{cookiecutter.project_slug}}/static/js/webpack_entry.js'],
    resolve: {
        extensions: ['*', '.js'],
    },
    output: {
        path: path.resolve('./{{cookiecutter.project_slug}}/static/js/bundles/'),
        filename: 'main.js',
    },
    module: {
        rules: [
            {
                test: /\.(js)$/,
                exclude: /node_modules/,
                use: ['babel-loader']
            }
        ]
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
        }),
    ]
};


