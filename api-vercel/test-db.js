const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = 'https://wbjbnfogbsiwqwnopocn.supabase.co';
const supabaseServiceKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndiamJuZm9nYnNpd3F3bm9wb2NuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MjI0Njk2MywiZXhwIjoyMDY3ODIyOTYzfQ.qgo76VLXsnXKfpxeTyYA7t76QIlEpsC4b5jv8HdY5ro';

const supabase = createClient(supabaseUrl, supabaseServiceKey);

async function testConnection() {
  try {
    console.log('Testing Supabase connection...');
    
    // 测试连接
    const { data, error } = await supabase
      .from('users')
      .select('count')
      .limit(1);
    
    if (error) {
      console.error('Database connection error:', error);
      return;
    }
    
    console.log('✅ Database connection successful!');
    console.log('Data:', data);
    
    // 检查表结构
    const { data: tables, error: tablesError } = await supabase
      .rpc('get_table_names');
    
    if (tablesError) {
      console.log('Cannot get table names, but connection works');
    } else {
      console.log('Tables:', tables);
    }
    
  } catch (error) {
    console.error('Test failed:', error);
  }
}

testConnection(); 