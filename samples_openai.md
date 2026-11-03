# Sample responses (openai mode)

### How do I verify as a student?

To verify as a student, you need to use a school email address or upload a current enrollment document. Verification typically takes under two minutes and can be reused at every participating store.

- Retrieved: student-docs, verify-how, expiry

### My verification failed, what now?

If your verification failed, check that your name matches your document exactly and that the document is not expired. You can retry up to three times, then contact support for manual review.

- Retrieved: failed, student-docs, verify-how

### Can I use two coupon codes on one order?

Member discounts usually cannot be combined with other coupon codes. You should check the store's terms on its page for any exceptions.

- Retrieved: promo-codes, stacking, gift-cards

### Where's my parcel?

I don't know. Please check the confirmation email from the store for order tracking details, or contact the store directly with your order number.

- Retrieved: order-status, shipping, returns

### Is it safe? Will shops see my personal info?

Yes, it is safe. Stores only learn that you belong to an eligible group and do not receive your personal documents or records.

- Retrieved: privacy, verify-how, promo-codes

### Can my spouse use my military discount?

Yes, military spouses can verify using service records and may be eligible for discounts.

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

I don't know. Please contact support for information regarding the weather.

- Retrieved: support, shipping, returns

### Write me a poem about cats

I don't know. Please contact support for assistance.

- Retrieved: failed, support, promo-codes
