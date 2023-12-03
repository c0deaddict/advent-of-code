{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    (pkgs.haskellPackages.ghcWithPackages (pkgs: with pkgs; [
      HUnit
      parsec
      raw-strings-qq
    ]))
  ];
}
