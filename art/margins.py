#!/usr/bin/env python3

"""\
Calculate how much space should go between the ends of the navbar banner and 
the right- and left-most links, such that this space is about half that between 
each link.
"""

link_widths = [
        36.747, # "Events"
        34.439, # "Travel"
        44.222, # "Lodging"
        45.190, # "Registry"
        39.866, # "Gallery"
        #42.974, # "Contact"
        29.066, # "RSVP"
]

banner_left = 19.950
banner_right = 532.633
banner_width = banner_right - banner_left

margin_width = banner_width - sum(link_widths)
num_half_margins = 2 * len(link_widths)
half_margin_width = margin_width / num_half_margins

print("Set the left coordinate of the outermost links as follows:")
print(f'  leftmost link:  {banner_left + half_margin_width:7.3f} px')
print(f'  rightmost link: {banner_left + banner_width - half_margin_width - link_widths[-1]:7.3f} px')
print("""
Once the outermost links are in position, distribute the links such that the 
horizontal gap between each is equal.""")




