# Sample responses (openai mode)

### How do I verify as a student?

To verify as a student, you can either use a school email address or upload a current enrollment document. Once verified, you can unlock member discounts in your account settings.

- Retrieved: student-docs, verify-how, expiry

### My verification failed, what now?

If your verification failed, check that your name matches your document exactly and that the document is not expired. You can retry up to three times, and if you still encounter issues, contact support for a manual review.

- Retrieved: failed, student-docs, verify-how

### Can I use two coupon codes on one order?

Member discounts usually cannot be combined with other coupon codes. For specific exceptions, please check the store's terms on its page.

- Retrieved: promo-codes, stacking, gift-cards

### Where's my parcel?

Order tracking is in the confirmation email from the store. Please check that email or contact the store directly with your order number for more information.

- Retrieved: order-status, shipping, returns

### Is it safe? Will shops see my personal info?

It is safe; shops only learn that you belong to an eligible group and do not receive your documents or personal records.

- Retrieved: privacy, verify-how, promo-codes

### Can my spouse use my military discount?

Yes, military spouses can use your military discount by verifying their service records.

- Retrieved: military, groups, gift-cards

### What discount does Nimbus Outdoors give?

Nimbus Outdoors offers a 20% discount for military members and students.

- Retrieved: stacking, groups, gift-cards
- Tool call: `get_discount` -> `{'store': 'Nimbus Outdoors', 'discount': '20%', 'groups': ['military', 'students']}`

### Which store has discounts for nurses?

I don't know which store has discounts for nurses. Please contact support for assistance.

- Retrieved: groups, stacking, gift-cards
- Tool call: `get_discount` -> `{'store': 'nurses', 'error': 'store not found'}`

### What's the weather in Paris?

I don't know. Please contact support for information on that topic.

- Retrieved: support, shipping, returns

### Write me a poem about cats

I don't know and suggest contacting support.

- Retrieved: failed, support, promo-codes
