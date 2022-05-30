{
  description =
    "A script running over all TLDs that fulfill specified requirements |check if `name.TLD` is still free.";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:

    flake-utils.lib.eachDefaultSystem (system:
      let pkgs = nixpkgs.legacyPackages.${system};

      in
      rec {

        formatter = pkgs.nixpkgs-fmt;

        packages = flake-utils.lib.flattenTree rec {

          domain-check = with pkgs.python39Packages;
            pkgs.python39Packages.buildPythonPackage rec {
              pname = "domain-check";
              version = "1.0.1";

              propagatedBuildInputs = [ requests ];
              buildInputs = [ pkgs.makeWrapper ];
              doCheck = false;
              src = self;

              postInstall = pkgs.lib.optional stdenv.isLinux ''
                wrapProgram $out/bin/domain-check --prefix PATH : ${
                  pkgs.lib.makeBinPath [ pkgs.dnsutils ]
                }
              '';

              meta = with pkgs.lib; {
                description =
                  "A script running over all TLDs that fulfill specified requirements.";
                homepage = "https://github.com/nonchris/domain-check";
                platforms = platforms.unix;
                maintainers = with maintainers; [ nonchris ];
              };
            };

        };
        defaultPackage = packages.domain-check;
      });
}
