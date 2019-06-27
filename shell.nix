with import <nixpkgs> {};

stdenv.mkDerivation {
  name = "env";
  buildInputs = with python3Packages; [
    python3
    cffi
    xen_4_12
  ];
}
