export interface Product {
  id: number;
  name: string;
  cost: string;
  count: number;
  cathegory_id: number;
}

export interface OrderProduct {
  id: number;
  count: number;
  product: Product;
}

export interface OrderProductPost {
  count: number;
  product_id: number;
}

export interface ProductPost {
  name: string;
  cost: string;
  count: number;
  cathegory_id: number;
}

export interface Cathegory {
  id: number;
  name: string;
}

export interface CathegoryPost {
  name: string;
}

export interface Order {
  id: number;
  name: string;
  phone: string;
  email: string;
  adress: string;
  pending: boolean;
  completed: boolean;
  products: OrderProduct[];
  created_at: string;
}

export interface OrderPost {
  name: string;
  phone: string;
  email: string;
  adress: string;
  products: OrderProductPost[];
}

export interface SearchResult {
  end: boolean;
  products: Product[];
}

type OrderByField = "name" | "cost" | "count";

export interface SearchParams {
  cathegory_id: number;
  in_stock_only: boolean;
  prompt: string;
  reversed: boolean;
  order_by: OrderByField;
}
