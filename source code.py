"""
Molecular Orbital Diagram Generator

"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


# =======================================================================
#  DATA CLASSES
# =======================================================================

class MolecularOrbital:
    """Represents a molecular orbital."""

    def __init__(self, name, energy, orbital_type, electrons=0):
        self.name = name
        self.energy = energy
        self.orbital_type = orbital_type  # 'bonding', 'antibonding', 'nonbonding'
        self.electrons = electrons  # 0, 1, or 2


class AtomicOrbital:
    """Represents an atomic orbital."""

    def __init__(self, name, energy, electrons=0):
        self.name = name
        self.energy = energy
        self.electrons = electrons


# =======================================================================
#  MO DIAGRAM GENERATOR CLASS
# =======================================================================

class MODiagramGenerator:
    """Main class to generate Molecular Orbital diagrams."""

    def __init__(self):
        # Configurations for supported molecules
        self.mo_configurations = {
            # ————— Simple 1s cases —————
            'H2': {'electrons': 2, 'ao_config': ['1s'], 'mo_order': ['σ1s', 'σ*1s'], 'category': 'simple'},
            'He2': {'electrons': 4, 'ao_config': ['1s'], 'mo_order': ['σ1s', 'σ*1s'], 'category': 'simple'},
            'He2+': {'electrons': 3, 'ao_config': ['1s'], 'mo_order': ['σ1s', 'σ*1s'], 'category': 'simple'},

            # ————— Light molecules (π2p < σ2p) —————
            'Li2': {'electrons': 6, 'ao_config': ['1s', '2s'], 'mo_order': ['σ1s', 'σ*1s', 'σ2s', 'σ*2s'], 'category': 'light'},
            'Be2': {'electrons': 8, 'ao_config': ['1s', '2s'], 'mo_order': ['σ1s', 'σ*1s', 'σ2s', 'σ*2s'], 'category': 'light'},
            'B2': {'electrons': 10, 'ao_config': ['1s', '2s', '2p'], 'mo_order': ['σ1s', 'σ*1s', 'σ2s', 'σ*2s', 'π2p', 'σ2p', 'π*2p', 'σ*2p'], 'category': 'light'},
            'C2': {'electrons': 12, 'ao_config': ['1s', '2s', '2p'], 'mo_order': ['σ1s', 'σ*1s', 'σ2s', 'σ*2s', 'π2p', 'σ2p', 'π*2p', 'σ*2p'], 'category': 'light'},
            'N2': {'electrons': 14, 'ao_config': ['1s', '2s', '2p'], 'mo_order': ['σ1s', 'σ*1s', 'σ2s', 'σ*2s', 'π2p', 'σ2p', 'π*2p', 'σ*2p'], 'category': 'light'},

            # ————— Heavier (σ2p < π2p) —————
            'O2': {'electrons': 16, 'ao_config': ['1s', '2s', '2p'], 'mo_order': ['σ1s', 'σ*1s', 'σ2s', 'σ*2s', 'σ2p', 'π2p', 'π*2p', 'σ*2p'], 'category': 'heavy'},
            'F2': {'electrons': 18, 'ao_config': ['1s', '2s', '2p'], 'mo_order': ['σ1s', 'σ*1s', 'σ2s', 'σ*2s', 'σ2p', 'π2p', 'π*2p', 'σ*2p'], 'category': 'heavy'},
            'Ne2': {'electrons': 20, 'ao_config': ['1s', '2s', '2p'], 'mo_order': ['σ1s', 'σ*1s', 'σ2s', 'σ*2s', 'σ2p', 'π2p', 'π*2p', 'σ*2p'], 'category': 'heavy'}
        }

        # Relative energies for MOs (light molecules)
        self.mo_energies = {
            'σ1s': -15, 'σ*1s': -13,
            'σ2s': -10, 'σ*2s': -8,
            'π2p': -5, 'σ2p': -4,
            'π*2p': -2, 'σ*2p': 0
        }

        # Modified energies for O2, F2, Ne2
        self.mo_energies_heavy = {
            'σ1s': -15, 'σ*1s': -13,
            'σ2s': -10, 'σ*2s': -8,
            'σ2p': -6, 'π2p': -5,
            'π*2p': -2, 'σ*2p': 0
        }

        # Atomic orbital energies
        self.ao_energies = {'1s': -14, '2s': -9, '2p': -4}

    # ===================================================================
    #  ELECTRON FILLING & BOND ORDER
    # ===================================================================

    def fill_electrons(self, molecule):
        """Fill electrons into MOs according to Aufbau principle."""

        if molecule not in self.mo_configurations:
            raise ValueError(f"Molecule {molecule} not in database")

        config = self.mo_configurations[molecule]
        total_electrons = config['electrons']
        category = config['category']
        mo_order = config['mo_order']

        # Choose proper energy ordering
        energies = self.mo_energies_heavy if category == 'heavy' else self.mo_energies

        # Build MO list
        mos = []
        for mo_name in mo_order:
            # π orbitals are doubly degenerate → max 4 electrons
            max_electrons = 4 if 'π' in mo_name else 2

            mos.append({
                'name': mo_name,
                'energy': energies[mo_name],
                'max_electrons': max_electrons,
                'electrons': 0,
                'is_antibonding': '*' in mo_name
            })

        # Fill electrons (no Hund's rule needed for simplified diagram)
        remaining = total_electrons
        for mo in mos:
            if remaining <= 0:
                break
            add = min(remaining, mo['max_electrons'])
            mo['electrons'] = add
            remaining -= add

        return mos

    def calculate_bond_order(self, molecule):
        """Calculate bond order = (bonding - antibonding)/2."""
        mos = self.fill_electrons(molecule)

        bonding_e = sum(mo['electrons'] for mo in mos if not mo['is_antibonding'])
        antibonding_e = sum(mo['electrons'] for mo in mos if mo['is_antibonding'])

        return (bonding_e - antibonding_e) / 2

    # ===================================================================
    #  DRAWING FUNCTIONS
    # ===================================================================

    def draw_electron(self, ax, x, y, spin='up'):
        """Draw an electron arrow."""
        arrow_length = 0.3
        if spin == 'up':
            ax.annotate('', xy=(x, y + arrow_length), xytext=(x, y - arrow_length),
                        arrowprops=dict(arrowstyle='->', color='blue', lw=2))
        else:
            ax.annotate('', xy=(x, y - arrow_length), xytext=(x, y + arrow_length),
                        arrowprops=dict(arrowstyle='->', color='red', lw=2))

    def draw_orbital_line(self, ax, x, y, width=0.8, color='black'):
        """Draw an orbital energy level line."""
        ax.plot([x - width/2, x + width/2], [y, y], color=color, linewidth=2)

    def draw_electrons_on_orbital(self, ax, x, y, electrons, is_pi=False):
        """Draw electrons on σ or π orbitals (π = degenerate pair)."""

        if is_pi:
            # π left & right
            spacing = 0.6

            # Left π orbital (max 2 e−)
            left = min(electrons, 2)
            if left >= 1:
                self.draw_electron(ax, x - spacing, y, 'up')
            if left == 2:
                self.draw_electron(ax, x - spacing + 0.15, y, 'down')

            # Right π orbital
            right = max(electrons - 2, 0)
            if right >= 1:
                self.draw_electron(ax, x + spacing, y, 'up')
            if right == 2:
                self.draw_electron(ax, x + spacing + 0.15, y, 'down')

        else:
            # σ orbital electrons
            if electrons >= 1:
                self.draw_electron(ax, x - 0.08, y, 'up')
            if electrons == 2:
                self.draw_electron(ax, x + 0.08, y, 'down')

    # ===================================================================
    #  MAIN DIAGRAM GENERATION
    # ===================================================================

    def generate_diagram(self, molecule, save_path=None):
        """Generate and display (or save) the MO diagram."""

        if molecule not in self.mo_configurations:
            print(f"Molecule '{molecule}' not found.")
            print("Available:", list(self.mo_configurations.keys()))
            return

        mos = self.fill_electrons(molecule)
        config = self.mo_configurations[molecule]
        bond_order = self.calculate_bond_order(molecule)

        # ------------------------------------------------------------------
        # Setup plot canvas
        # ------------------------------------------------------------------
        fig, ax = plt.subplots(figsize=(12, 10))
        ax.set_xlim(-3, 3)

        energies = [mo['energy'] for mo in mos]
        ax.set_ylim(min(energies) - 2, max(energies) + 2)

        # Column labels
        ax.text(-2, max(energies) + 0.5, f'Atom A\n({molecule[0]})', ha='center', fontsize=12, fontweight='bold')
        ax.text(0, max(energies) + 0.5, 'Molecular Orbitals', ha='center', fontsize=12, fontweight='bold')
        ax.text(2, max(energies) + 0.5, f'Atom B\n({molecule[0]})', ha='center', fontsize=12, fontweight='bold')

        # ------------------------------------------------------------------
        # Draw atomic orbitals (left & right)
        # ------------------------------------------------------------------
        for ao in config['ao_config']:
            ao_energy = self.ao_energies[ao]

            # Left
            self.draw_orbital_line(ax, -2, ao_energy, width=0.6, color='green')
            ax.text(-2.5, ao_energy, ao, ha='right', va='center', fontsize=10)

            # Right
            self.draw_orbital_line(ax, 2, ao_energy, width=0.6, color='green')
            ax.text(2.5, ao_energy, ao, ha='left', va='center', fontsize=10)

        # ------------------------------------------------------------------
        # Draw Molecular Orbitals (center)
        # ------------------------------------------------------------------
        for mo in mos:
            name = mo['name']
            energy = mo['energy']
            electrons = mo['electrons']
            is_pi = 'π' in name

            color = 'red' if '*' in name else 'blue'

            # Draw degenerate π orbitals
            if is_pi:
                self.draw_orbital_line(ax, -0.6, energy, width=0.5, color=color)
                self.draw_orbital_line(ax, 0.6, energy, width=0.5, color=color)
                ax.text(1.3, energy, name, va='center', fontsize=9)

            else:
                self.draw_orbital_line(ax, 0, energy, width=0.8, color=color)
                ax.text(0.6, energy, name, va='center', fontsize=9)

            # Plot electrons
            if electrons > 0:
                self.draw_electrons_on_orbital(ax, 0, energy, electrons, is_pi)

            # Dashed AO → MO mixing lines
            if '1s' in name:
                ao_e = self.ao_energies['1s']
            elif '2s' in name:
                ao_e = self.ao_energies['2s']
            elif '2p' in name:
                ao_e = self.ao_energies['2p']
            else:
                ao_e = energy

            ax.plot([-1.7, -0.4], [ao_e, energy], 'k--', alpha=0.3, linewidth=0.5)
            ax.plot([1.7, 0.4], [ao_e, energy], 'k--', alpha=0.3, linewidth=0.5)

        # ------------------------------------------------------------------
        # Info box: electrons, bond order, stability, magnetism
        # ------------------------------------------------------------------
        info_text = (
            f"Total Electrons: {config['electrons']}\n"
            f"Bond Order: {bond_order}\n"
        )

        stability = "Stable" if bond_order > 0 else "Unstable" if bond_order == 0 else "Does not exist"
        info_text += f"Stability: {stability}"

        # Magnetic behaviour
        unpaired = sum(
            1 for mo in mos
            if (('π' in mo['name'] and mo['electrons'] in [1, 3]) or
                ('π' not in mo['name'] and mo['electrons'] == 1))
        )

        if molecule == 'O2':
            info_text += "\nMagnetic: Paramagnetic (2 unpaired e⁻)"
        elif unpaired > 0:
            info_text += f"\nMagnetic: Paramagnetic ({unpaired} unpaired e⁻)"
        else:
            info_text += "\nMagnetic: Diamagnetic"

        ax.text(0.02, 0.02, info_text, transform=ax.transAxes,
                fontsize=11, va='bottom',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        # Legend
        ax.legend([
            mpatches.Patch(color='blue', label='Bonding MO'),
            mpatches.Patch(color='red', label='Antibonding MO'),
            mpatches.Patch(color='green', label='Atomic Orbital')
        ], loc='upper right')

        # Clean axes
        ax.set_ylabel('Energy →', fontsize=12)
        ax.set_xticks([])
        for spine in ['top', 'right', 'bottom']:
            ax.spines[spine].set_visible(False)

        plt.tight_layout()

        # Save if needed
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Diagram saved to {save_path}")

        plt.show()
        return bond_order


# =======================================================================
#  CLI ENTRY POINT
# =======================================================================

def main():
    """Interactive command-line interface."""

    print("=" * 60)
    print("     MOLECULAR ORBITAL DIAGRAM GENERATOR")
    print("=" * 60)

    gen = MODiagramGenerator()
    molecules = list(gen.mo_configurations.keys())

    print("\nAvailable molecules:")
    for i, mol in enumerate(molecules, 1):
        print(f"  {i}. {mol} (Bond Order: {gen.calculate_bond_order(mol)})")

    print("\n" + "-" * 60)

    while True:
        print("\nOptions:")
        print("  1. Generate diagram for a specific molecule")
        print("  2. Generate diagrams for all molecules")
        print("  3. Exit")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            molecule = input("Enter molecule formula (e.g., O2, N2, H2): ").strip()
            save = input("Save diagram? (y/n): ").strip().lower()
            save_path = f"{molecule}_MO_diagram.png" if save == 'y' else None
            gen.generate_diagram(molecule, save_path)

        elif choice == '2':
            for mol in molecules:
                print(f"\nGenerating diagram for {mol}...")
                gen.generate_diagram(mol, f"{mol}_MO_diagram.png")

        elif choice == '3':
            print("\nThank you for using the MO Diagram Generator!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
