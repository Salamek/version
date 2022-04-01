None (1.3) unstable; urgency=medium

  * Features
    * Changelog
      * afb2ab8 Added option to generate whole changelog

 -- Adam Schubert <adam.schubert@sg1-game.net>  Fri, 01 Apr 2022 14:46:57 +0000


None (1.2.18) unstable; urgency=medium

  * Fixes
    * Changelog
      * a88c2f6 Do not crash when original changelog was not found
      * 7ab98b6 Fix mkdir in Debian changelog generator

 -- Adam Schubert <adam.schubert@sg1-game.net>  Fri, 01 Apr 2022 14:46:57 +0000


None (1.2.16) unstable; urgency=medium

  * Features
    * Changelog
      * c73553c Added simple changelog CLI
  * Fixes
    * WhatIsNew
      * e36dae8 Call makdir only when path is in dir

 -- Adam Schubert <adam.schubert@sg1-game.net>  Fri, 01 Apr 2022 14:46:57 +0000


None (1.2.14) unstable; urgency=medium

  * Fixes
    * 
      * 1c71713 Fix when advancing major version, patch version was not reset
    * CI
      * 926c266 Remove old versions from arch repo correctly

 -- Adam Schubert <adam.schubert@sg1-game.net>  Fri, 01 Apr 2022 14:46:57 +0000


None (1.2.12) unstable; urgency=medium

  * Features
    * Log
      * 88d86db Simplify log format for better UX
    * CI
      * eeed86d Debian needs dh-python
  * Fixes
    * CI
      * 846970f Fix debian repo path

 -- Adam Schubert <adam.schubert@sg1-game.net>  Fri, 01 Apr 2022 14:46:57 +0000


None (1.2.10) unstable; urgency=medium

  * Features
    * Check
      * dfa87a7 Added option to force older version number
  * Fixes
    * CI
      * 7a6e8c9 Remove packagetest

 -- Adam Schubert <adam.schubert@sg1-game.net>  Fri, 01 Apr 2022 14:46:57 +0000


None (1.2.8) unstable; urgency=medium

  * Fixes
    * WhatIsNew
      * b4ab9d2 Fix crash when there is no tag in git repo

 -- Adam Schubert <adam.schubert@sg1-game.net>  Fri, 01 Apr 2022 14:46:57 +0000


None (1.2.6) unstable; urgency=medium

  * Nothing worth mentioning

 -- Adam Schubert <adam.schubert@sg1-game.net>  Fri, 01 Apr 2022 14:46:57 +0000


None (1.2.4) unstable; urgency=medium

  * Features
    * Changelog
      * c31b6f2 Implement WhatIsNew changelog generator

 -- Adam Schubert <adam.schubert@sg1-game.net>  Fri, 01 Apr 2022 14:46:57 +0000


None (1.2) unstable; urgency=medium

  * Features
    * Changelog
      * 634228d Added Debian changelog generator for #2

 -- Adam Schubert <adam.schubert@sg1-game.net>  Fri, 01 Apr 2022 14:46:57 +0000

None (1.3) unstable; urgency=medium

  * Features
    * Changelog
      * afb2ab8 Added option to generate whole changelog
      * c73553c Added simple changelog CLI
      * c31b6f2 Implement WhatIsNew changelog generator
      * 634228d Added Debian changelog generator for #2
    * Log
      * 88d86db Simplify log format for better UX
    * CI
      * eeed86d Debian needs dh-python
    * Check
      * dfa87a7 Added option to force older version number
  * Fixes
    * Changelog
      * a88c2f6 Do not crash when original changelog was not found
      * 7ab98b6 Fix mkdir in Debian changelog generator
    * WhatIsNew
      * e36dae8 Call makdir only when path is in dir
      * b4ab9d2 Fix crash when there is no tag in git repo
    * 
      * 1c71713 Fix when advancing major version, patch version was not reset
    * CI
      * 926c266 Remove old versions from arch repo correctly
      * 846970f Fix debian repo path
      * 7a6e8c9 Remove packagetest

 -- Adam Schubert <adam.schubert@sg1-game.net>  Fri, 01 Apr 2022 14:18:22 +0000

