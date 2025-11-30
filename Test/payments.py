# test_stripe_payment_automation.py
import stripe
import pytest
import requests
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Stripe
stripe.api_key = "sk_test_YOUR_TEST_SECRET_KEY"

class TestStripePaymentAutomation:
    """5+ Complete Stripe Payment Test Cases for Interview"""
    
    # ========== TEST CASE 1: POSITIVE - VISA Payment Success ==========
    def test_case_1_visa_payment_success(self):
        """✅ TEST CASE 1: Successful VISA Card Payment ($29.98)"""
        logger.info("\n🟢 TEST CASE 1: VISA Payment - Positive Scenario")
        
        # Step 1: Create Customer
        customer = stripe.Customer.create(
            email="stripe.test1@example.com",
            description="Test Customer - Case 1"
        )
        logger.info(f"✓ Customer created: {customer.id}")
        
        # Step 2: Create Payment Method (VISA)
        pm = stripe.PaymentMethod.create(
            type="card",
            card={
                "number": "4242424242424242",  # ✅ SUCCESS CARD
                "exp_month": 12,
                "exp_year": 2025,
                "cvc": "123"
            }
        )
        logger.info(f"✓ Payment method created: {pm.id}")
        assert pm.card.brand == "visa"
        
        # Step 3: Attach PM to Customer
        stripe.PaymentMethod.attach(pm.id, customer=customer.id)
        logger.info(f"✓ Payment method attached")
        
        # Step 4: Create One-Time Charge
        intent = stripe.PaymentIntent.create(
            amount=2998,  # $29.98
            currency="sgd",
            customer=customer.id,
            payment_method=pm.id,
            confirm=True,
            off_session=True,
            description="Premium OTT Subscription"
        )
        
        # Step 5: Verify Success
        assert intent.status == "succeeded"
        logger.info(f"✓ Payment succeeded!")
        logger.info(f"   - Amount: SGD 29.98")
        logger.info(f"   - Status: {intent.status}")
        logger.info(f"   - Charge ID: {intent.charges.data[0].id}")
        
        return True
    
    # ========== TEST CASE 2: DECLINED CARD - Error Handling ==========
    def test_case_2_declined_card_error_handling(self):
        """❌ TEST CASE 2: Handle Declined Card Gracefully"""
        logger.info("\n🔴 TEST CASE 2: Declined Card - Error Handling")
        
        customer = stripe.Customer.create(email="stripe.test2@example.com")
        
        # Use declined card
        pm = stripe.PaymentMethod.create(
            type="card",
            card={
                "number": "4000000000000002",  # ❌ DECLINE CARD
                "exp_month": 12,
                "exp_year": 2025,
                "cvc": "123"
            }
        )
        
        stripe.PaymentMethod.attach(pm.id, customer=customer.id)
        
        try:
            intent = stripe.PaymentIntent.create(
                amount=2998,
                currency="sgd",
                customer=customer.id,
                payment_method=pm.id,
                confirm=True,
                off_session=True
            )
            assert False, "Should have failed"
        except stripe.error.CardError as e:
            logger.info(f"✓ Card declined as expected")
            logger.info(f"   - Error Code: {e.code}")
            logger.info(f"   - Decline Code: {e.decline_code}")
            logger.info(f"   - Message: {e.user_message}")
            return True
    
    # ========== TEST CASE 3: IDEMPOTENCY - No Duplicate Charges ==========
    def test_case_3_idempotency_key(self):
        """🔒 TEST CASE 3: Idempotency - Prevent Duplicate Charges"""
        logger.info("\n🔒 TEST CASE 3: Idempotency Key Test")
        
        customer = stripe.Customer.create(email="stripe.test3@example.com")
        pm = stripe.PaymentMethod.create(
            type="card",
            card={"number": "4242424242424242", "exp_month": 12, "exp_year": 2025, "cvc": "123"}
        )
        stripe.PaymentMethod.attach(pm.id, customer=customer.id)
        
        # Create with Idempotency Key
        idempotency_key = f"subscription_{customer.id}_{datetime.now().timestamp()}"
        
        # First request
        intent1 = stripe.PaymentIntent.create(
            amount=2998,
            currency="sgd",
            customer=customer.id,
            payment_method=pm.id,
            confirm=True,
            off_session=True,
            idempotency_key=idempotency_key
        )
        
        # Second request with same key (should return same)
        intent2 = stripe.PaymentIntent.create(
            amount=2998,
            currency="sgd",
            customer=customer.id,
            payment_method=pm.id,
            confirm=True,
            off_session=True,
            idempotency_key=idempotency_key
        )
        
        # Verify same intent returned
        assert intent1.id == intent2.id
        logger.info(f"✓ Idempotency verified!")
        logger.info(f"   - Both requests returned same ID: {intent1.id}")
        logger.info(f"   - No duplicate charge created")
        
        return True
    
    # ========== TEST CASE 4: INSUFFICIENT FUNDS - Decline Code Handling ==========
    def test_case_4_insufficient_funds_decline(self):
        """💰 TEST CASE 4: Insufficient Funds Decline Handling"""
        logger.info("\n💰 TEST CASE 4: Insufficient Funds Scenario")
        
        customer = stripe.Customer.create(email="stripe.test4@example.com")
        
        # Insufficient funds card
        pm = stripe.PaymentMethod.create(
            type="card",
            card={
                "number": "4000000000009995",  # Insufficient funds
                "exp_month": 12,
                "exp_year": 2025,
                "cvc": "123"
            }
        )
        
        stripe.PaymentMethod.attach(pm.id, customer=customer.id)
        
        try:
            intent = stripe.PaymentIntent.create(
                amount=2998,
                currency="sgd",
                customer=customer.id,
                payment_method=pm.id,
                confirm=True,
                off_session=True
            )
        except stripe.error.CardError as e:
            assert e.decline_code == "insufficient_funds"
            logger.info(f"✓ Insufficient funds error caught!")
            logger.info(f"   - Decline Code: {e.decline_code}")
            logger.info(f"   - User Message: {e.user_message}")
            return True
    
    # ========== TEST CASE 5: MASTERCARD & Multiple Payment Methods ==========
    def test_case_5_mastercard_payment(self):
        """💳 TEST CASE 5: MasterCard Payment Processing"""
        logger.info("\n💳 TEST CASE 5: MasterCard Payment")
        
        customer = stripe.Customer.create(email="stripe.test5@example.com")
        
        # MasterCard
        pm = stripe.PaymentMethod.create(
            type="card",
            card={
                "number": "5555555555554444",  # MasterCard
                "exp_month": 12,
                "exp_year": 2025,
                "cvc": "123"
            }
        )
        
        stripe.PaymentMethod.attach(pm.id, customer=customer.id)
        
        intent = stripe.PaymentIntent.create(
            amount=2998,
            currency="sgd",
            customer=customer.id,
            payment_method=pm.id,
            confirm=True,
            off_session=True
        )
        
        assert intent.status == "succeeded"
        assert intent.charges.data[0].payment_method_details.card.brand == "mastercard"
        logger.info(f"✓ MasterCard payment successful!")
        logger.info(f"   - Brand: MasterCard")
        logger.info(f"   - Status: {intent.status}")
        
        return True
    
    # ========== TEST CASE 6: SUBSCRIPTION WITH AUTO-RENEWAL ==========
    def test_case_6_subscription_auto_renewal(self):
        """🔄 TEST CASE 6: Subscription Creation & Auto-Renewal"""
        logger.info("\n🔄 TEST CASE 6: Subscription Auto-Renewal")
        
        # Create customer
        customer = stripe.Customer.create(email="stripe.test6@example.com")
        
        # Create payment method
        pm = stripe.PaymentMethod.create(
            type="card",
            card={
                "number": "4242424242424242",
                "exp_month": 12,
                "exp_year": 2025,
                "cvc": "123"
            }
        )
        
        stripe.PaymentMethod.attach(pm.id, customer=customer.id)
        stripe.Customer.modify(customer.id, invoice_settings={"default_payment_method": pm.id})
        
        # Create product & price
        product = stripe.Product.create(name="Premium OTT Subscription")
        price = stripe.Price.create(
            product=product.id,
            unit_amount=2998,  # $29.98
            currency="sgd",
            recurring={"interval": "month", "interval_count": 1}
        )
        
        # Create subscription
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{"price": price.id}],
            billing_cycle_anchor=int((datetime.now() + timedelta(days=30)).timestamp())
        )
        
        assert subscription.status == "active"
        logger.info(f"✓ Subscription created!")
        logger.info(f"   - Subscription ID: {subscription.id}")
        logger.info(f"   - Status: {subscription.status}")
        logger.info(f"   - Current Period End: {datetime.fromtimestamp(subscription.current_period_end)}")
        logger.info(f"   - Auto-renewal: Enabled")
        
        return True
