import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.*;
import java.util.ArrayList;

public class StudentManagementUI extends JFrame {
    private JTextField idField, nameField, addressField;
    private JTable table;
    private DefaultTableModel tableModel;
    private ArrayList<Student> students;
    private static final String FILE_NAME = "students.data";

    public StudentManagementUI() {
        students = new ArrayList<>();
        loadStudents();

        setTitle("STUDENT MANAGEMENT");
        setSize(900, 400);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // Main panel with BorderLayout
        JPanel mainPanel = new JPanel(new BorderLayout());

        // Header panel (North)
        JPanel headerPanel = new JPanel();
        headerPanel.setBackground(new Color(173, 216, 230)); // Light blue background
        JLabel titleLabel = new JLabel("STUDENT MANAGEMENT", SwingConstants.CENTER);
        titleLabel.setFont(new Font("Arial", Font.BOLD, 24));
        headerPanel.add(titleLabel);
        mainPanel.add(headerPanel, BorderLayout.NORTH);

        // Left panel (West) with input fields and buttons
        JPanel leftPanel = new JPanel();
        leftPanel.setLayout(new BoxLayout(leftPanel, BoxLayout.Y_AXIS));
        leftPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        // Input fields
        JPanel inputPanel = new JPanel(new GridLayout(3, 2, 5, 5));
        inputPanel.add(new JLabel("ID:"));
        idField = new JTextField(15);
        inputPanel.add(idField);

        inputPanel.add(new JLabel("Name:"));
        nameField = new JTextField(15);
        inputPanel.add(nameField);

        inputPanel.add(new JLabel("Address:"));
        addressField = new JTextField(15);
        inputPanel.add(addressField);

        leftPanel.add(inputPanel);

        // Buttons panel
        JPanel buttonPanel = new JPanel(new GridLayout(3, 2, 5, 5));
        String[] buttonLabels = {"Add", "Delete", "Edit", "Search", "Clear", "Cancel"};
        for (String label : buttonLabels) {
            JButton button = new JButton(label);
            button.addActionListener(new ButtonClickListener());
            buttonPanel.add(button);
        }
        leftPanel.add(buttonPanel);

        mainPanel.add(leftPanel, BorderLayout.WEST);

        // Right panel (Center) with table
        String[] columnNames = {"ID", "Name", "Address"};
        tableModel = new NonEditableTableModel(columnNames, 0); // Sử dụng NonEditableTableModel
        table = new JTable(tableModel);
        JScrollPane scrollPane = new JScrollPane(table);
        mainPanel.add(scrollPane, BorderLayout.CENTER);

        add(mainPanel);
        setVisible(true);
        displayStudents();
    }

    // Lớp con của DefaultTableModel để vô hiệu hóa chỉnh sửa trực tiếp
    class NonEditableTableModel extends DefaultTableModel {
        public NonEditableTableModel(Object[] columnNames, int rowCount) {
            super(columnNames, rowCount);
        }

        @Override
        public boolean isCellEditable(int row, int column) {
            return false; // Không cho phép chỉnh sửa trực tiếp
        }
    }

    private class ButtonClickListener implements ActionListener {
        public void actionPerformed(ActionEvent e) {
            String command = e.getActionCommand();
            switch (command) {
                case "Add":
                    addStudent();
                    break;
                case "Delete":
                    deleteStudent();
                    break;
                case "Edit":
                    editStudent();
                    break;
                case "Search":
                    searchStudent();
                    break;
                case "Clear":
                    clearFields();
                    break;
                case "Cancel":
                    System.exit(0);
                    break;
            }
        }
    }

    private void addStudent() {
        String id = idField.getText();
        String name = nameField.getText();
        String address = addressField.getText();

        if (!id.isEmpty() && !name.isEmpty() && !address.isEmpty()) {
            // Kiểm tra xem ID đã tồn tại chưa
            boolean idExists = students.stream().anyMatch(student -> student.getId().equals(id));
            if (idExists) {
                JOptionPane.showMessageDialog(this, "ID already exists. Please use a different ID.");
            } else {
                students.add(new Student(id, name, address));
                saveStudents();
                clearFields();
                displayStudents();
            }
        } else {
            JOptionPane.showMessageDialog(this, "Please fill all fields.");
        }
    }

    private void deleteStudent() {
        String id = idField.getText();
        if (!id.isEmpty()) {
            students.removeIf(student -> student.getId().equals(id));
            saveStudents();
            clearFields();
            displayStudents();
        } else {
            JOptionPane.showMessageDialog(this, "Please enter an ID to delete.");
        }
    }

    private void editStudent() {
        String id = idField.getText();
        String name = nameField.getText();
        String address = addressField.getText();

        if (!id.isEmpty() && !name.isEmpty() && !address.isEmpty()) {
            boolean found = false;
            for (int i = 0; i < students.size(); i++) {
                Student student = students.get(i);
                if (student.getId().equals(id)) {
                    // Tạo một đối tượng Student mới với thông tin cập nhật
                    students.set(i, new Student(id, name, address));
                    found = true;
                    break;
                }
            }
            if (found) {
                saveStudents();
                clearFields();
                displayStudents();
            } else {
                JOptionPane.showMessageDialog(this, "Student not found.");
            }
        } else {
            JOptionPane.showMessageDialog(this, "Please fill all fields.");
        }
    }

    private void searchStudent() {
        String id = idField.getText();
        if (!id.isEmpty()) {
            for (Student student : students) {
                if (student.getId().equals(id)) {
                    tableModel.setRowCount(0);
                    tableModel.addRow(new Object[]{student.getId(), student.getName(), student.getAddress()});
                    return;
                }
            }
            JOptionPane.showMessageDialog(this, "Student not found.");
        } else {
            JOptionPane.showMessageDialog(this, "Please enter an ID to search.");
        }
    }

    private void clearFields() {
        idField.setText("");
        nameField.setText("");
        addressField.setText("");
        displayStudents();
    }

    private void displayStudents() {
        tableModel.setRowCount(0);
        for (Student student : students) {
            tableModel.addRow(new Object[]{student.getId(), student.getName(), student.getAddress()});
        }
    }

    private void saveStudents() {
        try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(FILE_NAME))) {
            oos.writeObject(students);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @SuppressWarnings("unchecked")
    private void loadStudents() {
        try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(FILE_NAME))) {
            students = (ArrayList<Student>) ois.readObject();
        } catch (IOException | ClassNotFoundException e) {
            students = new ArrayList<>();
        }
    }

    public static void main(String[] args) {
        new StudentManagementUI();
    }
}

