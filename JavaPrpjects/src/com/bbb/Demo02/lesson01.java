package com.bbb.Demo02;

import javax.xml.crypto.Data;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Random;
import java.util.Scanner;
import java.util.logging.SimpleFormatter;

public class lesson01 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        long n = 0;
        if (scanner.hasNextInt()) {
            n = scanner.nextInt();
        }
        int sum = 0;
        long startTime = System.nanoTime();
        for (int i = 0; i < n; i++) {
            sum += Math.pow(-1, i);
        }
        long endTime = System.nanoTime();
        System.out.println(endTime - startTime);
    }
}
