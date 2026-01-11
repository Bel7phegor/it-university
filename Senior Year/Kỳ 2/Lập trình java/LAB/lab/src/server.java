import java.io.*;
import java.net.*;

public class server {
    public static void main(String[] args) {
        final int PORT = 12345;
        
        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            System.out.println("Server is running on port " + PORT);
            
            while (true) {
                try (Socket clientSocket = serverSocket.accept();
                     BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                     PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true)) {
                    
                    System.out.println("Client connected: " + clientSocket.getInetAddress());
                    
                    // Read data from client
                    double a = Double.parseDouble(in.readLine());
                    double b = Double.parseDouble(in.readLine());
                    String operator = in.readLine();
                    
                    // Calculate result
                    double result = 0;
                    switch (operator) {
                        case "+":
                            result = a + b;
                            break;
                        case "-":
                            result = a - b;
                            break;
                        case "*":
                            result = a * b;
                            break;
                        case "/":
                            if (b != 0) {
                                result = a / b;
                            } else {
                                out.println("Error: Division by zero");
                                continue;
                            }
                            break;
                        default:
                            out.println("Error: Invalid operator");
                            continue;
                    }
                    
                    // Send result back to client
                    out.println(result);
                    System.out.println("Sent result: " + result);
                    
                } catch (NumberFormatException e) {
                    System.out.println("Invalid number format from client");
                } catch (IOException e) {
                    System.out.println("Error handling client: " + e.getMessage());
                }
            }
        } catch (IOException e) {
            System.out.println("Server exception: " + e.getMessage());
        }
    }
}