var gulp = require('gulp'),
    mjml = require('gulp-mjml'),
    connect = require('gulp-connect');
 
gulp.task('compile', function () {
  gulp.src('./mail.mjml')
    .pipe(mjml())
    .pipe(gulp.dest('.'))
    .pipe(connect.reload())
});

gulp.task('connect', function() {
  connect.server({
    root: './',
    livereload: true
  });
});

gulp.task('watch', function(){
	gulp.watch(['./*.mjml'],['compile'])
});

gulp.task('default', ['connect', 'watch']);
