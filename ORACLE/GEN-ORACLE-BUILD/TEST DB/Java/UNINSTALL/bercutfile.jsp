create or replace and compile java source named bercutfile as
import java.io.*;
import java.sql.*;
import java.util.Date;
import java.util.List;
import java.util.ArrayList;
import java.text.SimpleDateFormat;
import oracle.sql.BLOB;
import oracle.sql.CLOB;
import oracle.sql.ARRAY;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;
import java.util.zip.ZipOutputStream;
import java.util.zip.GZIPInputStream;
import java.util.zip.GZIPOutputStream;
import oracle.sql.ArrayDescriptor;

public class BercutFile {

  private static int SUCCESS = 0;
  private static int FAILURE = 1;
  private static int FILE_NOT_FOUND = 2;

/****************************************************************************
  Получение разделителя файлов
*****************************************************************************/
  public static String getFileSeparator() {
    return File.separator;
  }
/****************************************************************************
  Чтение списка файлов и папок из директории и вставка полученных данных
  во временную таблицу
*****************************************************************************/
  public static void getList(String directory) throws SQLException {
    File path = new File(directory);
    String[] list = path.list();
    String element;

    for(int i = 0; i < list.length; i++) {
      element = list[i];

      String fpath=directory + getFileSeparator() + list[i];
      File f = new File(fpath);

      long len;
      Date date;

      String ftype;
      String sqldate;

      SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

      if (f.isFile()) {
        len = f.length();
        date = new Date(f.lastModified());
        sqldate = df.format(date) ;
        ftype = "F";
      } else {
        len = 0;
        sqldate = null;
        ftype = "D";
      }

      #sql { INSERT INTO TMP$DIR_FILES (filename, filelength, filetype, filemodified, filepath)
             VALUES (:element, :len, :ftype, to_date(:sqldate,'YYYY-MM-DD HH24:MI:SS'), :fpath) };
    }
  }

/****************************************************************************
  Получение jdbc коннекта
*****************************************************************************/
  private static Connection getConnection() throws SQLException {
    Connection con = DriverManager.getConnection("jdbc:default:connection:");
    return con;
  }

/****************************************************************************
Сохраняет данные файла в CLOB
*****************************************************************************/
  public static CLOB file2clob(String fileName) throws SQLException, IOException {
    Connection con = null;
    CLOB clob = null;
    Writer writer = null;
    InputStream in = null;
    try {
      con = getConnection();
      clob = CLOB.createTemporary(con, true, CLOB.DURATION_SESSION);
      writer = clob.getCharacterOutputStream();
      in = new BufferedInputStream(new FileInputStream(new File(fileName)));
      byte[] buf = new byte[clob.getChunkSize()];
      int length;
      while ((length = in.read(buf)) != -1) {
        writer.write(new String(buf, 0, length));
      }
    } finally {
      if (in != null) {in.close();}
      if (writer != null) {writer.close();}
      if (con != null) {con.close();}
    }
    return clob;
  }

/****************************************************************************
Сохраняет данные файла в CLOB с указанной кодировкой
*****************************************************************************/
  public static CLOB file2clob(String fileName, String characterSet) throws SQLException, IOException {
    Connection con = null;
    CLOB clob = null;
    Writer writer = null;
    Reader reader = null;
    try {
      con = getConnection();
      clob = CLOB.createTemporary(con, true, CLOB.DURATION_SESSION);
      writer = clob.getCharacterOutputStream();
      reader = new InputStreamReader(
        new BufferedInputStream(new FileInputStream(new File(fileName))), characterSet
      );
      char[] chars = new char[clob.getChunkSize()];
      int iChar;
      while ((iChar = reader.read(chars)) != -1) {
        writer.write(chars, 0, iChar);
      }
    } finally {
      if (reader != null) {reader.close();}
      if (writer != null) {writer.close();}
      if (con != null) {con.close();}
    }
    return clob;
  }

/****************************************************************************
Сохраняет данные CLOB в указанный файл
*****************************************************************************/
  public static void clob2file(CLOB clob, String fileName)
    throws SQLException, IOException {
    Writer writer = null;
    Reader reader = null;
    try {
      writer = new BufferedWriter(new FileWriter(fileName));
      reader = new BufferedReader(clob.getCharacterStream());
      int length;
      char[] buf = new char[clob.getChunkSize()];
      while ((length = reader.read(buf, 0, clob.getChunkSize())) != -1) {
        writer.write(buf, 0, length);
      }
    } finally {
      if (writer != null) {writer.close();}
      if (reader != null) {reader.close();}
    }
  }

/****************************************************************************
Сохраняет данные CLOB в указанный файл с указанной кодировкой
*****************************************************************************/
  public static void clob2file(CLOB clob, String fileName, String characterSet)
    throws SQLException, IOException {
    Writer writer = null;
    Reader reader = null;
    try {
      writer = new OutputStreamWriter(
        new BufferedOutputStream(new FileOutputStream(new File(fileName))), characterSet
      );
      reader = new BufferedReader(clob.getCharacterStream());
      int length;
      char[] buf = new char[clob.getChunkSize()];
      while ((length = reader.read(buf, 0, clob.getChunkSize())) != -1) {
        writer.write(buf, 0, length);
      }
    } finally {
      if (writer != null) {writer.close();}
      if (reader != null) {reader.close();}
    }
  }

/****************************************************************************
Сохраняет данные файла в BLOB
*****************************************************************************/
  public static BLOB file2blob(String fileName) throws SQLException, IOException {
    Connection con = null;
    BLOB blob = null;
    OutputStream out = null;
    InputStream in = null;
    try {
      con = getConnection();
      blob = BLOB.createTemporary(con, true, BLOB.DURATION_SESSION);
      out = blob.getBinaryOutputStream();
      in = new BufferedInputStream(new FileInputStream(new File(fileName)));
      int length;
      int chunkSize = blob.getChunkSize();
      byte[] buf = new byte[chunkSize];
      while ((length = in.read(buf)) != -1) {
        out.write(buf, 0, length);
      }
    } finally {
      if (in != null) {in.close();}
      if (out != null) {out.close();}
      if (con != null) {con.close();}
    }
    return blob;
  }

/****************************************************************************
Сохраняет данные BLOB в указанный файл
*****************************************************************************/
  public static void blob2file(BLOB blob, String fileName)
  throws SQLException, IOException
  {
     InputStream in = null;
     OutputStream out = null;
     try {
        out = new BufferedOutputStream(new FileOutputStream(new File(fileName)));
        in = blob.getBinaryStream();
        int length;
        byte[] buf = new byte[blob.getChunkSize()];
        while ((length = in.read(buf)) != -1) {
           out.write(buf, 0, length);
        }
     }
     finally {
        if (in != null) {in.close();}
        if (out != null) {out.close();}
     }
  }

/****************************************************************************
  Удаление файла на сервере БД - указывается полный путь к файлу вместе с именем файла
  0 - файл удален успешно
  1 - ошибка удаления файла
  2 - файл не найден
*****************************************************************************/
  public static int deleteLocalFile(String fullFilename) {
    File file = new File(fullFilename);
    if (!file.exists()) {
      return FILE_NOT_FOUND;
    }
    try {
      if (!file.delete()) {
        return FAILURE;
      } else {
        return SUCCESS;
      }
    } catch (SecurityException ex) {
      throw new RuntimeException(ex);
    }
  }

/****************************************************************************
  Копирование файла
*****************************************************************************/
  public static int copy (String fromPath, String toPath) {
    try {
      File myFromFile = new File (fromPath);
      File myToFile   = new File (toPath);

      InputStream  in  = new FileInputStream(myFromFile);
      OutputStream out = new FileOutputStream(myToFile);

      byte[] buf = new byte[1024];
      int len;
      while ((len = in.read(buf)) > 0) {
        out.write(buf, 0, len);
      }
      in.close();
      out.close();
      return SUCCESS;
    } catch (Exception ex) {
      throw new RuntimeException(ex);
    }
  }

/****************************************************************************
  Проверка существования файла
*****************************************************************************/
  public static int exists (String path) {
    File myFile = new File (path);
    if (myFile.exists()) return SUCCESS; else return FAILURE;
  }

/****************************************************************************
  Получение списка файлов в zip архиве
*****************************************************************************/
  public static ARRAY getZippedFileNames(Blob zip) throws SQLException, IOException {
    ZipInputStream in = new ZipInputStream(zip.getBinaryStream());
    ZipEntry zipEntry;
    List<String> fileNames = new ArrayList();
    while ((zipEntry = in.getNextEntry()) != null) {
      if (!zipEntry.isDirectory()) {
        fileNames.add(zipEntry.getName());
      }
    }
    in.close();
    Connection con = getConnection();
    con.setAutoCommit(false);
    ArrayDescriptor descriptor = ArrayDescriptor.createDescriptor("VARCHAR2_TAB", con);
    return new ARRAY( descriptor, con, fileNames.toArray());
  }

/*****************************************************************************
Разархивирование из zip архива файла из переданного BLOB - результат возвращается в BLOB
****************************************************************************/
  public static Blob unzipFile(Blob zip, String fileName)
    throws SQLException, IOException {
    ZipInputStream in = new ZipInputStream(zip.getBinaryStream());
    ZipEntry zipEntry;
    BLOB result = null;
    while ((zipEntry = in.getNextEntry()) != null) {
      if (!zipEntry.isDirectory() & fileName.equalsIgnoreCase(zipEntry.getName())) {
        Connection con = getConnection();
        con.setAutoCommit(false);
        result = BLOB.createTemporary(con, true, BLOB.DURATION_SESSION);
        BufferedOutputStream out = new BufferedOutputStream(result.setBinaryStream(1));
        byte[] bytes = new byte[result.getChunkSize()];
        int count;
        while ((count = in.read(bytes, 0, bytes.length)) != -1) {
          out.write(bytes, 0, count);
        }
        out.close();
      }
    }
    in.close();
    return result;
  }

/*****************************************************************************
Разархивирование из gzip архива файла из переданного BLOB - результат возвращается в BLOB
****************************************************************************/
  public static Blob gunzipFile(Blob zip)
    throws SQLException, IOException {
    GZIPInputStream in = new GZIPInputStream(zip.getBinaryStream());
    BLOB result = null;
    Connection con = getConnection();
    con.setAutoCommit(false);
    result = BLOB.createTemporary(con, true, BLOB.DURATION_SESSION);
    BufferedOutputStream out = new BufferedOutputStream(result.setBinaryStream(1));
    int sChunk = 8192;
    byte[] buffer = new byte[sChunk];
    int length;
    while ((length = in.read(buffer, 0, sChunk)) != -1)
      out.write(buffer, 0, length);
    out.close();
    in.close();
    return result;
  }

/*****************************************************************************
Архивирование файла в ZIP
******************************************************************************/
  public static Blob zip(String fileName) throws SQLException, IOException {
     ZipOutputStream zipOut = null;
     File file = new File(fileName);
     InputStream in = null;
     BLOB result = null;
     try {
        in = new DataInputStream(new BufferedInputStream(new FileInputStream(file)));
        Connection con = getConnection();
        con.setAutoCommit(false);
        result = BLOB.createTemporary(con, true, BLOB.DURATION_SESSION);
        zipOut = new ZipOutputStream(new BufferedOutputStream(result.setBinaryStream(1)));
        zipOut.putNextEntry(new ZipEntry(file.getName()));
        byte[] b = new byte[(int) file.length()];
        int iCount;
        while ((iCount = in.read(b)) != -1) {
           zipOut.write(b, 0, iCount);
        }
     }
     finally {
        if (in != null) {
          in.close();
        }
        if (zipOut != null) {
          zipOut.close();
        }
     }
     return result;
  }

/*****************************************************************************
Архивирование файла в GZIP
******************************************************************************/
  public static Blob gzip(String fileName) throws SQLException, IOException {

     GZIPOutputStream gzipOut = null;
     File file = new File(fileName);
     InputStream in = null;
     BLOB result = null;
     try {
        in = new DataInputStream(new BufferedInputStream(new FileInputStream(file)));
        Connection con = getConnection();
        con.setAutoCommit(false);
        result = BLOB.createTemporary(con, true, BLOB.DURATION_SESSION);
        gzipOut = new GZIPOutputStream(new BufferedOutputStream(result.setBinaryStream(1)));
        byte[] b = new byte[(int) file.length()];
        int iCount;
        while ((iCount = in.read(b)) != -1) {
           gzipOut.write(b, 0, iCount);
        }
     }
     finally {
        if (in != null) {
          in.close();
        }
        if (gzipOut != null) {
          gzipOut.close();
        }
     }
     return result;
  }
}
/

