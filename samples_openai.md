# Sample responses (openai mode)

### How do I verify as a student?

To verify as a student, you can either use a school email address or upload a current enrollment document in your account settings. Verification usually takes under two minutes.

- Retrieved: student-docs, verify-how, expiry

### My verification failed, what now?

If your verification failed, check that your name matches your document exactly and that the document is not expired. You can retry up to three times, then contact support for manual review.

- Retrieved: failed, student-docs, verify-how

### Can I use two coupon codes on one order?

Member discounts usually cannot be combined with other coupon codes or clearance pricing. You should check the store's terms on its page for any exceptions.

- Retrieved: promo-codes, stacking, gift-cards

### Where's my parcel?

I don't know. You should check the order tracking in the confirmation email from the store or contact the store directly with your order number.

- Retrieved: order-status, shipping, returns

### Is it safe? Will shops see my personal info?

I don't know. You can contact support for more information on privacy and safety.

- Retrieved: privacy, verify-how, promo-codes

### Can my spouse use my military discount?

Yes, military spouses can verify using their service records to qualify for discounts.

- Retrieved: military, groups, gift-cards

### What discount does Nimbus Outdoors give?

Nimbus Outdoors offers a 20% discount for military members and students.

- Retrieved: stacking, groups, gift-cards
- Tool call: `get_discount` -> `{'store': 'Nimbus Outdoors', 'discount': '20%', 'groups': ['military', 'students']}`

### Which store has discounts for nurses?

Brightside Shoes has discounts for nurses.

- Retrieved: groups, stacking, gift-cards
- Tool call: `find_stores` -> `{'group': 'nurses', 'stores': ['Brightside Shoes']}`

### What's the weather in Paris?

I can only help with member discounts and shopping.

- Retrieved: support, shipping, returns

### Write me a poem about cats

I can only help with member discounts and shopping.

- Retrieved: failed, support, promo-codes
