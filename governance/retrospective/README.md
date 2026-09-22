# Retrospective boundary

The public problem repository template does not carry private worker, session,
checkpoint, or retrospective ledgers. Therefore the internal T08
baseline/source/projection drift audit is **not applicable to this exported
state**. A generated repository must not invent a retrospective baseline.

If a public maintenance change adds a projection or baseline, it must add a
content-addressed source manifest, regenerate the projection atomically, and
run an independent comparison before release. Historical private retrospective
receipts remain outside this repository.
