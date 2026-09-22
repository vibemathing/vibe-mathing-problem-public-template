# Security policy

Do not commit passwords, MFA codes, cookies, access tokens, private keys,
private host paths, or unpublished research records. Report a suspected
credential or boundary disclosure privately to the repository maintainers;
do not open a public issue containing the secret.

The release gate scans text, paths, symlinks, file modes, dependencies, and
package rights. A passing scan is not a substitute for human security review.
