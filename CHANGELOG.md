None (1.3.3) unstable; urgency=medium

  * Fixes
    * Changelog
      * 073b239 Debian changelog, generate date correctly

 -- Adam Schubert <adam.schubert@sg1-game.net>  Sat, 02 Apr 2022 17:06:10 +0000

None (1.3.2) unstable; urgency=medium

  * Fixes
    * Changelog
      * e53e115 Pull commits correctly when HEAD is used

 -- Adam Schubert <adam.schubert@sg1-game.net>  Fri Apr 1 16:59:16 2022 +0200


None (1.3.1) unstable; urgency=medium

  * Fixes
    * Sematic
      * faba815 Handle situations when tag is not created yet
  * Features
    * Changelog
      * afb2ab8 Added option to generate whole changelog

 -- Adam Schubert <adam.schubert@sg1-game.net>  Fri Apr 1 16:46:57 2022 +0200


None (1.2.18) unstable; urgency=medium

  * Fixes
    * Changelog
      * a88c2f6 Do not crash when original changelog was not found
      * 7ab98b6 Fix mkdir in Debian changelog generator

 -- Adam Schubert <adam.schubert@sg1-game.net>  Fri Apr 1 14:03:30 2022 +0200


None (1.2.16) unstable; urgency=medium

  * Features
    * Changelog
      * c73553c Added simple changelog CLI
  * Fixes
    * WhatIsNew
      * e36dae8 Call makdir only when path is in dir

 -- Adam Schubert <adam.schubert@sg1-game.net>  Fri Apr 1 13:50:54 2022 +0200


None (1.2.14) unstable; urgency=medium

  * Fixes
    * 
      * 1c71713 Fix when advancing major version, patch version was not reset
    * CI
      * 926c266 Remove old versions from arch repo correctly

 -- Adam Schubert <adam.schubert@sg1-game.net>  Wed Oct 13 23:46:41 2021 +0200


None (1.2.12) unstable; urgency=medium

  * Features
    * Log
      * 88d86db Simplify log format for better UX
    * CI
      * eeed86d Debian needs dh-python
  * Fixes
    * CI
      * 846970f Fix debian repo path

 -- Adam Schubert <adam.schubert@sg1-game.net>  Mon Aug 23 18:31:38 2021 +0200


None (1.2.10) unstable; urgency=medium

  * Features
    * Check
      * dfa87a7 Added option to force older version number
  * Fixes
    * CI
      * 7a6e8c9 Remove packagetest

 -- Adam Schubert <adam.schubert@sg1-game.net>  Mon Aug 23 16:29:44 2021 +0200


None (1.2.8) unstable; urgency=medium

  * Fixes
    * WhatIsNew
      * b4ab9d2 Fix crash when there is no tag in git repo

 -- Adam Schubert <adam.schubert@sg1-game.net>  Tue Jun 15 23:10:53 2021 +0200


None (1.2.6) unstable; urgency=medium

  * Nothing worth mentioning

 --    


None (1.2.4) unstable; urgency=medium

  * Features
    * Changelog
      * c31b6f2 Implement WhatIsNew changelog generator

 -- Adam Schubert <adam.schubert@sg1-game.net>  Mon Feb 17 19:14:55 2020 +0100


None (1.2) unstable; urgency=medium

  * Features
    * Changelog
      * 634228d Added Debian changelog generator for #2

 -- Adam Schubert <adam.schubert@sg1-game.net>  Thu Oct 24 01:07:02 2019 +0200

