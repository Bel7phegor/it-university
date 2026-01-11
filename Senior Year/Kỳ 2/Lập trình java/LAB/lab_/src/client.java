import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.net.*;

public class TCPClientGUI extends JFrame {
    private JTextField num1Field, num2Field, resultField;
    private JComboBox<String> operatorCombo;
    private JButton calculateButton;
    
    public TCPClientGUI() {
        setTitle("TCP Calculator Client");
        setSize(400, 250);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new GridLayout(5, 2, 10, 10));
        
        // Create components
        add(new JLabel("Nhập số thứ nhất:"));
        num1Field = new JTextField();
        add(num1Field);
        
        add(new JLabel("Nhập số thứ hai:"));
        num2Field = new JTextField();
        add(num2Field);
        
        add(new JLabel("Chọn phép toán:"));
        operatorCombo = new JComboBox<>(new String[]{"+", "-", "*", "/"});
        add(operatorCombo);
        
        add(new JLabel("Kết quả:"));
        resultField = new JTextField();
        resultField.setEditable(false);
        add(resultField);
        
        calculateButton = new JButton("Tính toán");
        calculateButton.addActionListener(new CalculateListener());
        add(calculateButton);
        
        setVisible(true);
    }
    
    private class CalculateListener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e) {
            final String SERVER_IP = "localhost";
            final int PORT = 12345;
            
            try {
                double a = Double.parseDouble(num1Field.getText());
                double b = Double.parseDouble(num2Field.getText());
                String operator = (String) operatorCombo.getSelectedItem();
                
                try (Socket socket = new Socket(SERVER_IP, PORT);
                     PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
                     BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()))) {
                    
                    // Send data to server
                    out.println(a);
                    out.println(b);
                    out.println(operator);
                    
                    // Get and display result
                    String response = in.readLine();
                    resultField.setText(response);
                    
                } catch (UnknownHostException ex) {
                    JOptionPane.showMessageDialog(null, "Server not found: " + ex.getMessage());
                } catch (IOException ex) {
                    JOptionPane.showMessageDialog(null, "I/O error: " + ex.getMessage());
                }
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(null, "Vui lòng nhập số hợp lệ");
            }
        }
    }
    
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new TCPClientGUI());
    }
}