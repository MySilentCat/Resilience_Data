var graph = {
    "data": [
        {
            "name": "User",
            "id": "User",
            "symbolSize": 45,
            "category": 1,
            "CGBR": 1.02,
            "marginal_prob": 0.64,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        },
        {
            "name": "Front_end",
            "id": "Front_end",
            "symbolSize": 45,
            "category": 1,
            "CGBR": 0.85,
            "marginal_prob": 0.64,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        },
        {
            "name": "Li",
            "id": "Li",
            "symbolSize": 45,
            "category": 1,
            "CGBR": 0.88825,
            "marginal_prob": 0.64,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        },
        {
            "name": "Shop",
            "id": "Shop",
            "symbolSize": 45,
            "category": 1,
            "CGBR": 0.85,
            "marginal_prob": 0.64,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        },
        {
            "name": "Order",
            "id": "Order",
            "symbolSize": 45,
            "category": 1,
            "CGBR": 0.93075,
            "marginal_prob": 0.64,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        },
        {
            "name": "Inquire",
            "id": "Inquire",
            "symbolSize": 45,
            "category": 1,
            "CGBR": 0.88825,
            "marginal_prob": 0.64,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        },
        {
            "name": "Shoppinng",
            "id": "Shoppinng",
            "symbolSize": 45,
            "category": 1,
            "CGBR": 0.88825,
            "marginal_prob": 0.64,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        },
        {
            "name": "Management",
            "id": "Management",
            "symbolSize": 45,
            "category": 1,
            "CGBR": 0.9369125,
            "marginal_prob": 0.64,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        },
        {
            "name": "Database",
            "id": "Database",
            "symbolSize": 45,
            "category": 1,
            "CGBR": 1.441036875,
            "marginal_prob": 0.3963468365781761,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        },
        {
            "name": "Pay",
            "id": "Pay",
            "symbolSize": 45,
            "category": 1,
            "CGBR": 0.8944124999999999,
            "marginal_prob": 0.4096,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        },
        {
            "name": "Attack0",
            "id": "Attack0",
            "symbolSize": 45,
            "category": 0,
            "CGBR": 0,
            "marginal_prob": 0.6,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        },
        {
            "name": "Attack1",
            "id": "Attack1",
            "symbolSize": 45,
            "category": 0,
            "CGBR": 0,
            "marginal_prob": 0.6,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        },
        {
            "name": "Attack2",
            "id": "Attack2",
            "symbolSize": 45,
            "category": 0,
            "CGBR": 0,
            "marginal_prob": 0.6,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        },
        {
            "name": "Attack3",
            "id": "Attack3",
            "symbolSize": 45,
            "category": 0,
            "CGBR": 0,
            "marginal_prob": 0.6,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        },
        {
            "name": "Reliability",
            "id": "Reliability",
            "symbolSize": 45,
            "category": 2,
            "CGBR": 0,
            "marginal_prob": 0.497341072816522,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        },
        {
            "name": "Restoration",
            "id": "Restoration",
            "symbolSize": 45,
            "category": 2,
            "CGBR": 0,
            "marginal_prob": 0.497341072816522,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        },
        {
            "name": "Resilience",
            "id": "Resilience",
            "symbolSize": 45,
            "category": 3,
            "CGBR": 0,
            "marginal_prob": 0.49734107281652207,
            "fixed": false,
            "itemStyle": {
                "normal": {
                    "opacity": 1
                }
            }
        }
    ],
    "categories": [
        {
            "name": "Attack Node"
        },
        {
            "name": "Component Node"
        },
        {
            "name": "Resilience Sub Attribute Node"
        },
        {
            "name": "Resilience Node"
        }
    ],
    "links": [
        {
            "source": "User",
            "target": "Li",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.2,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "User",
            "target": "Order",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.2,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "User",
            "target": "Inquire",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.2,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "User",
            "target": "Shoppinng",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.2,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "User",
            "target": "Reliability",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.2,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "User",
            "target": "Restoration",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.2,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Front_end",
            "target": "User",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.2,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Li",
            "target": "Database",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.2,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Shop",
            "target": "User",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.2,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Shop",
            "target": "Order",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.2,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Shop",
            "target": "Management",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.2,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Order",
            "target": "Database",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.2,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Inquire",
            "target": "Database",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.2,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Shoppinng",
            "target": "Management",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.2,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Shoppinng",
            "target": "Database",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.2,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Shoppinng",
            "target": "Pay",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.2,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Management",
            "target": "Database",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.2,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Database",
            "target": "Reliability",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.2,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Database",
            "target": "Restoration",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.2,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Attack0",
            "target": "Front_end",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.2,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Attack1",
            "target": "Shop",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.2,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Attack2",
            "target": "Database",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.2,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Attack3",
            "target": "Pay",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.2,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Reliability",
            "target": "Resilience",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.2,
                    "type": "solid",
                    "opacity": 1
                }
            }
        },
        {
            "source": "Restoration",
            "target": "Resilience",
            "symbol": [
                "none",
                "arrow"
            ],
            "lineStyle": {
                "normal": {
                    "width": 2,
                    "curveness": 0.2,
                    "type": "solid",
                    "opacity": 1
                }
            }
        }
    ]
}