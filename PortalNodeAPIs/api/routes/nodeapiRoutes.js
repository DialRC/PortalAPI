'use strict';
module.exports = function(app) {
  var yourchatbot = require('../bot/toyBot');

  // nodeapi Routes
  app.route('/init')
    .post(yourchatbot.init);

  app.route('/next')
    .post(yourchatbot.next);

  app.route('/end')
    .post(yourchatbot.end);
};