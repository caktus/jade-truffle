const gulp = require("gulp");
const rename = require("gulp-rename");
const webpack = require("webpack-stream");

gulp.task('javascript', function() {
  return gulp
    .src("./{{cookiecutter.project_app}}/assets/js/webpack_entry.js")
    .pipe(webpack(require("./webpack.config.js")))
    .pipe(rename("main.js"))
    .pipe(gulp.dest("./{{cookiecutter.project_app}}/static/js/"));
});

gulp.task('watch-js', function(done) {
  gulp.watch(["./apps/{{cookiecutter.primary_app}}/assets/js/**/*.js"], gulp.series("javascript"));
  done();
})

{% if cookiecutter.css_style == "tailwind" %}

gulp.task('styles', function() {
  const postcss = require("gulp-postcss");
  const tailwindcss = require("tailwindcss");

  return gulp
    .src("./{{cookiecutter.project_app}}/assets/styles/tailwind_entry.css")
    .pipe(
      postcss([
        require("postcss-import"),
        require("postcss-preset-env"),
        tailwindcss("./tailwind.config.js"),
        require("autoprefixer"),
      ])
    )
    .pipe(rename("main.css"))
    .pipe(gulp.dest("./{{cookiecutter.project_app}}/static/css/"));
});

gulp.task('watch-css', function(done) {
  gulp.watch(
    [
      './apps/{{cookiecutter.primary_app}}/**/*.css',
      './tailwind.config.js'
    ], gulp.series('styles')
  )
  done();
});

{% else %}
gulp.task('styles', function() {
  const sass = require('gulp-sass')(require('sass'));
  return gulp
    .src("./{{cookiecutter.project_app}}/assets/styles/sass_entry.scss")
    .pipe(sass().on('error', sass.logError))
    .pipe(rename("main.css"))
    .pipe(gulp.dest("./{{cookiecutter.project_app}}/static/css/"));
});

gulp.task('watch-css', function(done) {
  gulp.watch(
    [
    './{{cookiecutter.project_app}}/assets/styles/sass_entry.scss',
    './apps/{{cookiecutter.primary_app}}/assets/styles/sass/**/*.scss'
    ], gulp.series('styles')
  );
  done();
});
{% endif %}


exports.default = gulp.series('styles', 'javascript', 'watch-css', 'watch-js');