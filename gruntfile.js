'use strict';

module.exports = function(grunt) {
  grunt.initConfig({
    connect: {
      server: {
        options: {
          base: ['.'],
          hostname: 'localhost',
          port: 8000,
          keepalive: true
        }
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-connect');

  grunt.registerTask('default', ['connect']);
};
