"""
Author : zhifenghan

Date : 2025/05/10

Function : This script is used to test multi attack

"""

def attack_cases():
    print("Start ICARUS single link attack.")
    import samples.attack.ICARUS.single_link as SINGLE_LINK
    SINGLE_LINK.single_link_attack()
    print("Single link attack is completed.")
    print()

    print("Start ICARUS multi link attack.")
    import samples.attack.ICARUS.mul_link as MULTI_LINK
    MULTI_LINK.multi_link_attack()
    print("Multi link attack is completed.")
    print()

    print("Start StarMelt energy drain attack.")
    import samples.attack.StarMelt.energy_drain as ENERGY_DRAIN
    ENERGY_DRAIN.energy_drain()
    print("Energy drain attack is completed.")
    print()

if __name__ == '__main__':
    attack_cases()
