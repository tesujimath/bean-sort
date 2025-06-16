{
  description = "Development and CI for bean-sort";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = inputs:
    inputs.flake-utils.lib.eachDefaultSystem
      (system:
        let
          pkgs = import inputs.nixpkgs {
            inherit system;
          };

          ci-packages = with pkgs; [
            bashInteractive
            python311
            uv
          ];

          bean-sort =
            let pyproject = (builtins.fromTOML (builtins.readFile ./pyproject.toml));
            in
            pkgs.python311Packages.buildPythonApplication {
              pname = "bean-sort";
              version = pyproject.project.version;
              pyproject = true;
              src = ./.;

              buildInputs = [ pkgs.python311Packages.flit-core ];
            };
        in
        with pkgs;
        {
          devShells.default = mkShell {
            nativeBuildInputs = ci-packages;
          };

          packages.default = bean-sort;
        }
      );
}
