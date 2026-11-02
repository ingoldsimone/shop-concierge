# Sample responses (openai mode)

### How do I verify as a student?

To verify as a student, use a school email address or upload a current enrollment document in your account settings. Verification usually takes under two minutes.

- Retrieved: student-docs, verify-how, expiry

### My verification failed, what now?

If your verification fails, check that your name matches your document exactly and that the document is not expired. You can retry up to three times. If it still fails, contact support for manual review.

- Retrieved: failed, student-docs, verify-how

### Can I use two coupon codes on one order?

Member discounts usually cannot be combined with other coupon codes. You should check the store's terms for any exceptions.

- Retrieved: promo-codes, stacking, gift-cards

### Where's my parcel?

I don't know. Please check the order tracking link in your confirmation email or contact the store directly with your order number for details.

- Retrieved: order-status, shipping, returns

### Is it safe? Will shops see my personal info?

It is safe. Shops only learn that you belong to an eligible group and do not receive your documents or personal records.

- Retrieved: privacy, verify-how, promo-codes

### Can my spouse use my military discount?

Yes, military spouses can verify using the service records and may be eligible for discounts.

- Retrieved: military, groups, gift-cards

### What discount does Nimbus Outdoors give?

Nimbus Outdoors offers a 20% discount to military members and students.

- Retrieved: stacking, groups, gift-cards
- Tool call: `get_discount` -> `{'store': 'Nimbus Outdoors', 'discount': '20%', 'groups': ['military', 'students']}`

### Which store has discounts for nurses?

Brightside Shoes offers discounts for nurses.

- Retrieved: groups, stacking, gift-cards
- Tool call: `find_stores` -> `{'group': 'nurses', 'stores': ['Brightside Shoes']}`

### What's the weather in Paris?

I don't know. Please contact support.

- Retrieved: support, shipping, returns

### Write me a poem about cats

I'm sorry, but I can't assist with that. Please contact support for help.

- Retrieved: failed, support, promo-codes
