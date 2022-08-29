// Require Gulp
var gulp = require('gulp');
var sass = require('gulp-sass');
var sourcemaps = require('gulp-sourcemaps');
var prefix = require('gulp-autoprefixer');
var watch = require('gulp-watch');
var critical = require('critical');

// Gulp Sass Task
gulp.task('sass', function () {
  gulp
    .src('_sass/*_/_.scss')
    .pipe(sourcemaps.init()) // Initializes sourcemaps
    .pipe(
      sass({
        errLogToConsole: true,
        outputStyle: 'compressed',
      }),
    )
    .pipe(prefix('last 2 versions', '> 1%', 'ie 8'))
    .pipe(sourcemaps.write('./')) // Writes sourcemaps into the CSS file
    .pipe(gulp.dest('gulpcss'));
});

gulp.task('critical', function () {
  critical.generate({
    base: './',
    src: '_site/index.html',
    css: '_site/css/screen.css',
    dest: '_includes/critical.css',
    width: 320,
    height: 480,
    minify: true,
  });
});

gulp.task('watch', function () {
  gulp.watch('_sass/*_/_.scss', ['sass']);
});

gulp.task('default', ['sass', 'watch']);
