export interface Product {
  id: number;
  name: string;
  cost: string;
  count: number;
  cathegory_id: number;
  description: string | null;
}

export interface ProductPost {
  name: string;
  cost: string;
  count: number;
  cathegory_id: number;
  description: string | null;
}
