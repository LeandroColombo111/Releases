'use strict';

module.exports = {
  parserOpts: {
    headerPattern: /^\[DS-(\d+)\] - (.*):(.*)$/,
    headerCorrespondence: ['ticket', 'type', 'subject']
  },
  releaseRules: [
    {type: 'feat', release: 'minor'},
    {type: 'fix', release: 'patch'},
    {type: 'chore', release: 'patch'}
  ],
  writerOpts: {
    transform: (commit, context) => {
      if (!commit.type || !commit.subject) {
        return;
      }

      const issues = [];

      commit.notes.forEach(note => {
        note.title = 'BREAKING CHANGES';
      });

      return commit;
    }
  }
};
