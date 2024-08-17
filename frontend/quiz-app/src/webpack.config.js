const webpack = require('webpack');

module.exports = {
  plugins: [
    new webpack.DefinePlugin({
      'process.env.REACT_APP_QUIZZES_API': JSON.stringify(
        process.env.ENV === 'prod' || process.env.ENV === 'dev'
          ? `https://oga-${process.env.ENV}.onrender.com/api/v1/quizzes`
          : 'http://localhost:5000/api/v1/quizzes'
      )
    })
  ],
  devServer: {
    client: {
      overlay: true,
      progress: true,
    },
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  },
};
