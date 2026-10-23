package main;

import model.Stock;

public class Main {

    public static void main(String[] args) {

        Stock stock = new Stock(
                "Reliance Industries",
                "RELIANCE",
                1400,
                1900000,
                24.5
        );

        System.out.println("=== MarketLens ===");
        System.out.println(stock);
    }
}