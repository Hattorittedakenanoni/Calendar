import { useEffect, useState } from 'react';
import { getCompanies } from './api/companies';

function CompanyList() {
  const [companies, setCompanies] = useState([]); 

  useEffect(() => {
    getCompanies()
      .then(setCompanies)
      .catch(console.error);
  }, []);

  return (
    <ul>
      {companies.map(company => (
        <li key={company.id}>
          {company.name}
        </li>
      ))}
    </ul>
  );
}

export default CompanyList;
