# Internal reference

Content does not carry internal-deployment references that an openly-published,
organization-neutral corpus should not expose. The check scans for internal-domain
hostnames (a name ending in `.local`, `.internal`, `.corp`, `.lan`, `.intranet`, or
`home.arpa`, excluding filenames whose stem ends in one of those words before a file
extension), cloud-region identifiers (AWS, Azure, and GCP region shapes), and CIDR
subnets outside the documentation, private, and reserved ranges. Lines inside fenced
code blocks are skipped. The detection regexes and the documentation-subnet filter
are fixed in the check implementation; the scanned-suffix set and the exempt-file set
(files that document the internal-reference formats by design, including the check's
own source) are project configuration. Content matching no pattern contributes no
findings.
