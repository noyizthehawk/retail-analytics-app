"""Standard column names for retail order-level data."""

from __future__ import annotations

import re
from typing import Final, Iterable

# --- Required columns -----------------------------------

ORDER_DATE: Final = "order_date"
ORDER_ID: Final = "order_id"
PRODUCT_ID: Final = "product_id"
QUANTITY: Final = "quantity"
UNIT_PRICE: Final = "unit_price"

# --- Column types (for validation) ----------------------

REQUIRED_NUMERIC_COLUMNS: Final[tuple[str, ...]] = (QUANTITY, UNIT_PRICE)
REQUIRED_DATE_COLUMNS: Final[tuple[str, ...]] = (ORDER_DATE,)
REQUIRED_TEXT_COLUMNS: Final[tuple[str, ...]] = (ORDER_ID, PRODUCT_ID)

REQUIRED_COLUMNS: Final[tuple[str, ...]] = (
    *REQUIRED_DATE_COLUMNS,
    *REQUIRED_TEXT_COLUMNS,
    *REQUIRED_NUMERIC_COLUMNS,
)

# --- Optional columns -----------------------------------

CUSTOMER_ID: Final = "customer_id"
SALES: Final = "sales"
PROFIT: Final = "profit"
DISCOUNT: Final = "discount"
CATEGORY: Final = "category"
REGION: Final = "region"
COUNTRY: Final = "country"
SUB_CATEGORY: Final = "sub_category"
SEGMENT: Final = "customer_segment"
SHIP_MODE: Final = "ship_mode"
PRODUCT_NAME: Final = "product_name"
STATE: Final = "state"
CITY: Final = "city"
POSTAL_CODE: Final = "postal_code"



OPTIONAL_NUMERIC_COLUMNS: Final[tuple[str, ...]] = (DISCOUNT, PROFIT, SALES)
OPTIONAL_TEXT_COLUMNS: Final[tuple[str, ...]] = (
    CUSTOMER_ID,
    PRODUCT_NAME,
    COUNTRY,
    REGION,
    CATEGORY,
    SUB_CATEGORY,
    SEGMENT,
    SHIP_MODE,
    STATE,
    CITY,
    POSTAL_CODE,
)

OPTIONAL_COLUMNS: Final[tuple[str, ...]] = (
    *OPTIONAL_NUMERIC_COLUMNS,
    *OPTIONAL_TEXT_COLUMNS,
)

STANDARD_COLUMNS: Final[tuple[str, ...]] = REQUIRED_COLUMNS + OPTIONAL_COLUMNS

# Common header variants from uploaded CSVs -> canonical names
COLUMN_ALIASES: Final[dict[str, str]] = {
    # order_date
    "date": ORDER_DATE,
    "order date": ORDER_DATE,
    "order_dt": ORDER_DATE,
    "transaction_date": ORDER_DATE,
    "invoice date": ORDER_DATE,
    "invoice_date": ORDER_DATE,
    # order_id
    "order": ORDER_ID,
    "order number": ORDER_ID,
    "order_no": ORDER_ID,
    "order_num": ORDER_ID,
    "transaction_id": ORDER_ID,
    "invoice": ORDER_ID,
    "invoice no": ORDER_ID,
    "invoice_no": ORDER_ID,
    "invoice number": ORDER_ID,
    # product_id
    "sku": PRODUCT_ID,
    "product id": PRODUCT_ID,
    "stockcode": PRODUCT_ID,
    "stock code": PRODUCT_ID,
    # quantity
    "qty": QUANTITY,
    "units": QUANTITY,
    # unit_price
    "price": UNIT_PRICE,
    "unit price": UNIT_PRICE,
    "unit_cost": UNIT_PRICE,
    "unit cost": UNIT_PRICE,
    # customer_id
    "customer": CUSTOMER_ID,
    "customer id": CUSTOMER_ID,
    "cust_id": CUSTOMER_ID,
    "client_id": CUSTOMER_ID,
    # sales
    "revenue": SALES,
    "amount": SALES,
    "sale": SALES,
    "total_sales": SALES,
    "sales_amount": SALES,
    # profit
    "margin": PROFIT,
    "net_profit": PROFIT,
    "profit_amount": PROFIT,
    # optional
    "disc": DISCOUNT,
    "discount_amount": DISCOUNT,
    "cat": CATEGORY,
    "product_category": CATEGORY,
    "geo": REGION,
    "state": STATE,
    "city": CITY,
    'postal code': POSTAL_CODE,
    "postal_code": POSTAL_CODE,
    "subcategory": SUB_CATEGORY,
    "sub_category": SUB_CATEGORY,
    "segment": SEGMENT,
    "customer segment": SEGMENT,
    "ship mode": SHIP_MODE,
    "shipping_mode": SHIP_MODE,
    "product": PRODUCT_NAME,
    "item": PRODUCT_NAME,
    "product name": PRODUCT_NAME,
}


def _normalize_key(name: str) -> str:
    """Normalize a raw header for alias lookup.

    Handles snake_case, kebab-case, spaces, and camelCase / PascalCase
    (e.g. invoiceDate, InvoiceDate, OrderID -> invoice date, order id).
    """
    key = name.strip()
    # invoiceDate -> invoice Date, OrderID -> Order ID, HTTPResponse -> HTTP Response
    key = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", key)
    key = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", key)
    key = key.lower()
    key = re.sub(r"[\s\-_]+", " ", key)
    return key.strip()


def canonical_column_name(name: str) -> str:
    """Map a raw header to the app's canonical column name."""
    key = _normalize_key(name)
    if key in COLUMN_ALIASES:
        return COLUMN_ALIASES[key]
    # Already canonical or unknown — use snake_case form
    return key.replace(" ", "_")


def normalize_column_names(columns: Iterable[str]) -> list[str]:
    """Return canonical names for a sequence of raw headers."""
    return [canonical_column_name(c) for c in columns]


def missing_required_columns(columns: Iterable[str]) -> list[str]:
    """Return required standard columns that are not present."""
    present = {canonical_column_name(c) for c in columns}
    return [col for col in REQUIRED_COLUMNS if col not in present]


def present_optional_columns(columns: Iterable[str]) -> list[str]:
    """Return optional standard columns that are present."""
    present = {canonical_column_name(c) for c in columns}
    return [col for col in OPTIONAL_COLUMNS if col in present]
