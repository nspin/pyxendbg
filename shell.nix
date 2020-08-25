with import <nixpkgs> {};

mkShell {
  nativeBuildInputs = with python3Packages; [
    python3
    cffi
    xen_4_12
  ];
  shellHook = ''
    buildBindings() {
      python3 bindings/build.py
    }
  '';
}
